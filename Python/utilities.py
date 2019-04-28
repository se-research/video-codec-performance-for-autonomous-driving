import os
from skopt.space import Integer, Categorical
from skopt.utils import use_named_args
import threading
import csv

CID = '112'
SHARED_MEMORY_AREA = 'video1'

STOP_AFTER = 80
TIMED_OUT_MSG_BYTES = str.encode('[frame-feed-evaluator]: Timed out while waiting for encoded frame.\n')
TIMED_OUT = 0

PNGS_PATH = os.path.join(os.getcwd(), '../2019-03-22_AstaZero_RuralRoad')
OUTPUT_REPORT_PATH = os.path.join(os.getcwd(), 'reports')

PREFIX_COLOR_FFE = '92'
PREFIX_COLOR_ENCODER = '94'

max_ssim = 0


# Iterates the generator and prints its log and sets violation TIMED_OUT
def log_helper(log_generator, color):
    for x in log_generator:
        print('\033[' + color + 'm### \033[0m' + (str(x, 'utf-8')))  # Prints with color code prefix and in utf-8
        if x == TIMED_OUT_MSG_BYTES:
            global TIMED_OUT
            TIMED_OUT = 1


# Saves list in output_name as name, creates dir output_path if not already exists
def save_list(list, output_path, name):
    if os.path.isdir(output_path):
        best_config_file = open(output_path + '/' + name, 'w')  # opens/creates file
        best_config_file.writelines(list)
        print("Best parameters saved: " + output_path + '/' + name)
    else:
        try:
            os.mkdir(output_path)
            best_config_file = open(output_path + '/' + name, 'w')  # opens/creates file
            best_config_file.writelines(list)
            print("Best parameters saved: " + output_path + '/' + name)
        except Exception as e:
            print("Creation of the dir %s failed. " + e % output_path)


# Returns coordinates so that the cropping will grow from the center/bottom line
def calculate_crop_x(INITIAL_WIDTH, width):
    return str(int(INITIAL_WIDTH) / 2 - (int(width) / 2))


def calculate_crop_y(INITIAL_HEIGHT, height):
    return str(int(INITIAL_HEIGHT) - (int(height)))


class FFE:
    def __init__(self, init_width='0', init_height='0', width='0', height='0', report_name='not_set'):
        self.init_width = init_width
        self.init_height = init_height
        self.width = width
        self.height = height
        self.report_name = report_name

    REPO = 'https://github.com/chrberger/frame-feed-evaluator.git'
    VERSION = 'v0.0.4'
    TAG = 'ffe:' + VERSION

    VOLUMES = {'/tmp/': {'bind': '/tmp', 'mode': 'rw'},
               OUTPUT_REPORT_PATH: {'bind': '/host', 'mode': 'rw'},
               PNGS_PATH: {
                   'bind': '/pngs',
                   'mode': 'rw'}
               }

    def get_commands(self):
        return ['--folder=/pngs',
                '--report=' + self.report_name,
                '--cid=' + CID,
                '--name=' + SHARED_MEMORY_AREA,
                '--crop.x=' + calculate_crop_x(self.init_width, self.width),
                '--crop.y=' + calculate_crop_y(self.init_height, self.height),
                '--crop.width=' + self.width,
                '--crop.height=' + self.height,
                '--delay=0',
                '--delay.start=150',
                '--stopafter=' + str(STOP_AFTER),
                # '--noexitontimeout'
                # '--verbose',
                ]


class H264:
    def __init__(self, init_width='0', init_height='0', resolution=['VGA', '640', '480'], config=0, docker_client=None):
        self.init_width = init_width
        self.init_height = init_height
        self.resolution = resolution[0]
        self.width = resolution[1]
        self.height = resolution[2]
        self.config = config
        self.docker_client = docker_client

    REPO = 'https://github.com/chalmers-revere/opendlv-video-h264-encoder.git'
    VERSION = 'v0.0.2'
    TAG = 'h264:' + VERSION

    PARAMETERS = (
        'bitrate', 'bitrate_max', 'gop', 'rc_mode', 'ecomplexity', 'sps_pps_strategy', 'num_ref_frame', 'ssei',
        'prefix_nal', 'entropy_coding', 'frame_skip', 'qp_max', 'qp_min', 'long_term_ref', 'loop_filter', 'denoise',
        'background_detection', 'adaptive_quant', 'frame_cropping', 'scene_change_detect', 'padding'
    )

    # https://www.web3.lu/avc-h264-video-settings/ # https://www.pixeltools.com/rate_control_paper.html
    # https://superuser.com/questions/638069/what-is-the-maximum-and-minimum-of-q-value-in-ffmpeg
    # https://slhck.info/video/2017/02/24/crf-guide.html
    # All parameters available in h264 and their ranges
    SPACE = [Integer(100000, 5000000, name='bitrate'),
             Integer(100000, 5000000, name='bitrate_max'),
             Integer(1, 250, name='gop'),
             Integer(-1, 3, name='rc_mode'),
             Integer(0, 2, name='ecomplexity'),
             Categorical((0, 1, 2, 3, 6), name='sps_pps_strategy'),
             Integer(1, 16, name='num_ref_frame'),
             Integer(0, 1, name='ssei'),
             Integer(0, 1, name='prefix_nal'),
             Integer(0, 1, name='entropy_coding'),
             Integer(0, 1, name='frame_skip'),
             Integer(0, 51, name='qp_max'),  # fix
             Integer(0, 50, name='qp_min'),  # fix
             Integer(0, 1, name='long_term_ref'),
             Integer(0, 2, name='loop_filter'),
             Integer(0, 1, name='denoise'),
             Integer(0, 1, name='background_detection'),
             Integer(0, 1, name='adaptive_quant'),
             Integer(0, 1, name='frame_cropping'),
             Integer(0, 1, name='scene_change_detect'),
             Integer(0, 1, name='padding')
             ]

    @use_named_args(SPACE)
    def objective(self, bitrate, bitrate_max, gop, rc_mode, ecomplexity, sps_pps_strategy, num_ref_frame, ssei,
                  prefix_nal, entropy_coding, frame_skip, qp_max, qp_min, long_term_ref, loop_filter, denoise,
                  background_detection, adaptive_quant, frame_cropping, scene_change_detect, padding):

        # update report name with this iteration's config
        # global config
        report_name = 'ffe-AstaZero_Rural_Road-' + self.TAG + '-' + self.resolution + '-' + 'C' + str(
            self.config) + '.csv'
        self.config += 1

        global TIMED_OUT
        TIMED_OUT = 0  # resets violation variable

        def get_list_encoder():
            return ['--cid=' + CID,
                    '--name=' + SHARED_MEMORY_AREA,
                    '--width=' + self.width,
                    '--height=' + self.height,
                    '--rc-mode=1',
                    '--bitrate=' + str(bitrate),
                    '--bitrate-max=' + str(bitrate_max),
                    '--gop=' + str(gop),
                    '--rc-mode=' + str(rc_mode),
                    '--ecomplexity=' + str(ecomplexity),
                    '--sps_pps_strategy=' + str(sps_pps_strategy),
                    '--num_ref_frame=' + str(num_ref_frame),
                    '--ssei=' + str(ssei),
                    '--prefix-nal=' + str(prefix_nal),
                    '--entropy-coding' + str(entropy_coding),
                    '--frame-skip=' + str(frame_skip),
                    '--qp-max=' + str(qp_max),
                    '--qp-min=' + str(qp_min),
                    '--long-term-ref' + str(long_term_ref),
                    '--loop-filter=' + str(loop_filter),
                    '--denoise' + str(denoise),
                    '--background-detection=' + str(background_detection),
                    '--adaptive_quant' + str(adaptive_quant),
                    '--frame-cropping' + str(frame_cropping),
                    '--scene-change-detect=' + str(scene_change_detect),
                    '--padding=' + str(padding),
                    # '--verbose'
                    ]

        try:  # try/catch to catch when the containers crash due to illegal parameter combination
            container_ffe = self.docker_client.containers.run(FFE.TAG,
                                                              command=FFE.get_commands(),
                                                              volumes=FFE.VOLUMES,
                                                              environment=['DISPLAY=:0'],
                                                              working_dir='/host',
                                                              network_mode="host",
                                                              ipc_mode="host",
                                                              remove=True,
                                                              detach=True,
                                                              )

            container_encoder = self.docker_client.containers.run(self.TAG,
                                                                  command=get_list_encoder(),
                                                                  volumes={'/tmp': {'bind': '/tmp', 'mode': 'rw'}},
                                                                  network_mode="host",
                                                                  ipc_mode="host",
                                                                  remove=True,
                                                                  detach=True
                                                                  )
            thread_logs_ffe = threading.Thread(target=log_helper,
                                               args=[container_ffe.logs(stream=True), PREFIX_COLOR_FFE])
            thread_logs_encoder = threading.Thread(target=log_helper, args=[container_encoder.logs(stream=True),
                                                                            PREFIX_COLOR_ENCODER])
            thread_logs_ffe.start()
            thread_logs_encoder.start()

            thread_logs_ffe.join()  # Blocks execution until both threads has terminated
            thread_logs_encoder.join()  # @TODO  Change to have the actual containers, encoder and ffe, blocking

        except Exception as e:
            print(e)
            print("Most likely an illegal encoder config combination")
            try:
                container_ffe.kill()  # ensures that both containers are killed to not get conflicts for new containers
                container_encoder.kill()
                return 1  # returns 1 as SSIM in case of crash (inverted due to minimization algorithm)
            except Exception as e:
                print(e)
                return 1  # returns 1 as SSIM in case of crash (inverted due to minimization algorithm)

        if TIMED_OUT:  # FFE timed out due to size or compression time constraint violated
            print("TIMED OUT")
            return 1  # returns 1 (inverted due to minimization algorithm)

        file = open(OUTPUT_REPORT_PATH + '/' + report_name, 'r')  # opens report generated
        plots = csv.reader(file, delimiter=';')
        sum = 0
        length = 0
        for row in plots:
            sum += float(row[10])  # accomulate values in SSIM column
            length += 1

        avg = sum / length  # computes SSIM average

        global max_ssim
        if avg > max_ssim:  # if the new mean ssim is the best so far, update max_ssim and best_config variables
            max_ssim = avg
            global best_config
            best_config = report_name

        return 1 - avg  # subtracts mean SSIM from 1 since the algorithm tries to find the minimum
