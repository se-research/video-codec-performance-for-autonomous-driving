from skopt.space import Integer, Categorical
from skopt.utils import use_named_args
from statistics import mean
import signal
import threading
import csv
import utilities
import FFE
import inspect

_local_variables = {}

REPO = 'https://github.com/chalmers-revere/opendlv-video-h264-encoder.git'
VERSION = 'v0.0.2'
TAG = 'h264:' + VERSION

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


# Parameter names for appending the best configuration.
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
         Integer(0, 4, name='rc_mode'),
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


@use_named_args(SPACE)
def objective(bitrate, bitrate_max, gop, rc_mode, ecomplexity, sps_pps_strategy, num_ref_frame, ssei,
              prefix_nal, entropy_coding, frame_skip, qp_max, qp_min, long_term_ref, loop_filter, denoise,
              background_detection, adaptive_quant, frame_cropping, scene_change_detect, padding):

    parameters = []
    frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)
    for i in args:
        parameters.append(str(i) + ': ' + str(values[i]) + '\n')

    utilities.save_config(parameters, utilities.get_report_name())

    print('Using ' + TAG + ' to encode ' + utilities.get_dataset_name())
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
        
        # Timeout handling on hanged container.
        def handler(signum, frame):
            print('Signal handler called with signal', signum)
            container_ffe.kill()
            container_encoder.kill()

        # Setup alarm on threads, if the container does not terminate before 
        # the get_system_timeout a kill signal is called.
        # Only availible on unix systems. 
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(utilities.get_system_timeout())

        thread_logs_ffe.start()
        thread_logs_encoder.start()

        thread_logs_ffe.join()  # Blocks execution until both threads has terminated
        thread_logs_encoder.join()

        # Disable the alarm
        signal.alarm(0)

    except Exception as e:
        print(e)
        print("Most likely an illegal encoder config combination")
        try:
            container_ffe.kill()  # Ensures that both containers are killed to not get conflicts for new containers
            container_encoder.kill()
            return utilities.MAX_VIOLATION  # Returns MAX_VIOLATION as SSIM in case of crash
        except Exception as e:
            print(e)
            return utilities.MAX_VIOLATION

    # FFE timed out due to compression time constraint violated
    if utilities.get_time_out():
        print('--------- TIMED OUT ---------')
        return utilities.MAX_VIOLATION

    file = open(utilities.get_output_report_path() + '/' + _local_variables['report_name'], 
                'r')  # Opens generated report
    report_file = csv.reader(file, delimiter=';')

    time_violations=[]
    ssim =[]
    for row in report_file:
        ssim.append(float(row[10]))  # Accumulate values in SSIM column in csv
        time = float(row[12])   # Extract compression time from csv

        if time > 40000:    # If compression time is more than the allowed 40 ms
            time_violations.append(time)

    frames = len(ssim) + 1 # Account for the one frame that some encoders do not encode

    # Return MAX_VIOLATION if dropped frames are more than MAX_DROPPED_FRAMES
    if frames / (utilities.get_dataset_lenght()) < utilities.MAX_DROPPED_FRAMES:
        print('--------- DROPPED FRAMES EXCEEDED MAX_DROPPED_FRAMES ---------')
        return utilities.MAX_VIOLATION

    if time_violations: 
        return mean(time_violations) / 40000 # Returns mean of violation time (between 1 and MAX_VIOLATION)

    if not ssim:
        print('--------- EMPTY FILE ---------')
        return utilities.MAX_VIOLATION

    ssim_mean = mean(ssim)  # Computes SSIM average
    if ssim_mean > utilities.get_max_ssim():  # Update max_ssim & best_config_name variable
        utilities.set_max_ssim(ssim_mean)
        utilities.set_best_config_name(_local_variables['report_name'])

    return 1 - ssim_mean  # Subtracts mean SSIM from 1 since the algorithm tries to find the minimum
