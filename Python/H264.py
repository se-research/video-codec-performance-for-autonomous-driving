from skopt.space import Integer, Categorical
from skopt.utils import use_named_args
from statistics import mean
import threading
import csv
import utilities
import FFE


_local_variables = {}


def set_report_name(name):
    _local_variables['report_name'] = name


def initialize(init_width='0', init_height='0', resolution=['VGA', '640', '480'], docker_client=None,
               report_name='not_set_in_encoder'):
    _local_variables['init_width'] = init_width
    _local_variables['init_height'] = init_height
    _local_variables['resolution_name'] = resolution[0]
    _local_variables['width'] = resolution[1]
    _local_variables['height'] = resolution[2]
    _local_variables['docker_client'] = docker_client
    _local_variables['report_name'] = report_name


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
         Categorical((0, 1), name='ssei'),
         Categorical((0, 1), name='prefix_nal'),
         Categorical((0, 1), name='entropy_coding'),
         Categorical((0, 1), name='frame_skip'),
         Integer(0, 51, name='qp_max'),  # fix
         Integer(0, 50, name='qp_min'),  # fix
         Categorical((0, 1), name='long_term_ref'),
         Integer(0, 2, name='loop_filter'),
         Categorical((0, 1), name='denoise'),
         Categorical((0, 1), name='background_detection'),
         Categorical((0, 1), name='adaptive_quant'),
         Categorical((0, 1), name='frame_cropping'),
         Categorical((0, 1), name='scene_change_detect'),
         Categorical((0, 1), name='padding')
         ]


def get_default_encoder_config():
    return [1500000,  # bitrate
            5000000,  # max_bitrate
            10,  # qop
            0,  # rc_mode
            0,  # ecomplexity
            0,  # sps_pps_strategy
            1,  # num_ref_frame
            0,  # ssei
            0,  # prefix_nal
            0,  # entropy_coding
            1,  # frame_skip
            42,  # qp_max
            12,  # qp_min
            0,  # long_term_ref
            0,  # loop_filter
            0,  # denoise
            1,  # background_detection
            1,  # adaptive_quant
            1,  # frame_cropping
            1,  # scene_change_detect
            1,  # padding
            ]


@use_named_args(SPACE)
def objective(bitrate, bitrate_max, gop, rc_mode, ecomplexity, sps_pps_strategy, num_ref_frame, ssei,
              prefix_nal, entropy_coding, frame_skip, qp_max, qp_min, long_term_ref, loop_filter, denoise,
              background_detection, adaptive_quant, frame_cropping, scene_change_detect, padding):

    print(TAG)
    utilities.reset_time_out()  # resets violation variable

    try:  # try/catch to catch when the containers crash due to illegal parameter combination
        def get_list_encoder():
            return ['--cid=' + utilities.CID,
                    '--name=' + utilities.SHARED_MEMORY_AREA,
                    '--width=' + _local_variables['width'],
                    '--height=' + _local_variables['height'],
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
                    '--threads=4'
                    #'--verbose'
                    ]

        container_ffe = _local_variables['docker_client'].containers.run(FFE.TAG,
                                                                         command=FFE.get_commands(),
                                                                         volumes=FFE.get_volumes(),
                                                                         environment=['DISPLAY=:0'],
                                                                         working_dir='/host',
                                                                         network_mode="host",
                                                                         ipc_mode="host",
                                                                         remove=True,
                                                                         detach=True,
                                                                         )

        container_encoder = _local_variables['docker_client'].containers.run(TAG,
                                                                             command=get_list_encoder(),
                                                                             volumes={'/tmp': {'bind': '/tmp',
                                                                                               'mode': 'rw'}},
                                                                             network_mode="host",
                                                                             ipc_mode="host",
                                                                             remove=True,
                                                                             detach=True
                                                                             )
        thread_logs_ffe = threading.Thread(target=utilities.log_helper,
                                           args=[container_ffe.logs(stream=True), utilities.PREFIX_COLOR_FFE])
        thread_logs_encoder = threading.Thread(target=utilities.log_helper, args=[container_encoder.logs(stream=True),
                                                                                  utilities.PREFIX_COLOR_ENCODER])
        thread_logs_ffe.start()
        thread_logs_encoder.start()

        thread_logs_ffe.join()  # Blocks execution until both threads has terminated
        thread_logs_encoder.join()

    except Exception as e:
        print(e)
        print("Most likely an illegal encoder config combination")
        try:
            container_ffe.kill()  # ensures that both containers are killed to not get conflicts for new containers
            container_encoder.kill()
            return utilities.MAX_VIOLATION  # returns MAX_VIOLATION as SSIM in case of crash
        except Exception as e:
            print(e)
            return utilities.MAX_VIOLATION

    if utilities.get_time_out():  # FFE timed out due to compression time constraint violated
        print('--------- TIMED OUT ---------')
        return utilities.MAX_VIOLATION

    file = open(utilities.get_output_report_path() + '/' + _local_variables['report_name'], 'r')  # opens report generated
    plots = csv.reader(file, delimiter=';')

    time_violations=[]
    ssim =[]
    for row in plots:
        ssim.append(float(row[10]))  # accomulate values in SSIM column

        time = float(row[12])
        if time > 40000:  # scales violation time up to 250 % (2.5) violation
            time_violations.append(time)

    if time_violations:  # if the list is not empty
        return mean(time_violations) / 40000

    if not ssim:  # if the list is empty
        print('--------- EMPTY FILE ---------')
        return utilities.MAX_VIOLATION

    ssim_mean = mean(ssim)  # computes SSIM average
    if ssim_mean > utilities.get_max_ssim():  # update max_ssim & best_config_name variable
        utilities.set_max_ssim(ssim_mean)
        utilities.set_best_config_name(_local_variables['report_name'])

    return 1 - ssim_mean  # subtracts mean SSIM from 1 since the algorithm tries to find the minimum
