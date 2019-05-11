 
from skopt.space import Integer, Categorical
from skopt.utils import use_named_args
from statistics import mean
import signal
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

REPO = 'https://github.com/chalmers-revere/opendlv-video-vpx-encoder.git'
VERSION = 'v0.0.7'
TAG = 'vp9:' + VERSION

PARAMETERS = (
    'gop', 'drop_frame', 'resize_allowed', 'resize_up', 'resize_down',
    'undershoot_pct', 'overshoot_pct', 'min_q', 'end_usage', 'buffer_size', 'buffer_init_size', 'buffer_optimal_size', 'bitrate',
    'kf_mode', 'kf_min_dist', 'kf_max_dist'
)

# http://doxygen.db48x.net/mozilla/html/structvpx__codec__enc__cfg.html
# Parameters according to https://www.webmproject.org/docs/encoder-parameters/
SPACE = [Integer(1, 250, name='gop'),
         Integer(0, 100, name='drop_frame'),
         Categorical((0, 1), name='resize_allowed'),
         Integer(0, 100, name='resize_up'),
         Integer(0, 100, name='resize_down'),
         Integer(0, 100, name='undershoot_pct'),
         Integer(0, 100, name='overshoot_pct'),
         Integer(0, 52, name='min_q'),
         Categorical((0, 1), name='end_usage'),
         Integer(0, 6000, name='buffer_size'),
         Integer(0, 4000, name='buffer_init_size'),
         Integer(0, 5000, name='buffer_optimal_size'),
         Integer(100000, 5000000, name='bitrate'),
         Categorical((0, 1), name='kf_mode'),
         Categorical((0, 1), name='kf_min_dist'),
         Integer(0, 250, name='kf_max_dist')
         ]


def get_default_encoder_config(resolution):
    if resolution == 'VGA':
        return [26,  # gop
                67,  # drop_frame
                0,  # resize_allowed
                87,  # resize_up
                30,  # resize_down
                22,  # undershoot_pct
                85,  # overshoot_pct
                17,  # min_q
                1,  # end_usage
                3264,  # buffer_size
                3268,  # buffer_init_size
                3519, # buffer_optimal_size
                2168373,  # bitrate
                1,  # kf_mode
                0,  # kf_min_dist
                93,  # kf_max_dist
                ]
    elif resolution == 'SVGA':
        return [159,  # gop
                0,  # drop_frame
                1,  # resize_allowed
                0,  # resize_up
                93,  # resize_down
                95,  # undershoot_pct
                16,  # overshoot_pct
                13,  # min_q
                0,  # end_usage
                6000,  # buffer_size
                1147,  # buffer_init_size
                0, # buffer_optimal_size
                3895523,  # bitrate
                1,  # kf_mode
                1,  # kf_min_dist
                163,  # kf_max_dist
                ]
    elif resolution == 'XGA':
        return [68,  # gop
                18,  # drop_frame
                1,  # resize_allowed
                90,  # resize_up
                100,  # resize_down
                31,  # undershoot_pct
                31,  # overshoot_pct
                44,  # min_q
                1,  # end_usage
                5425,  # buffer_size
                4000,  # buffer_init_size
                1445, # buffer_optimal_size
                2194015,  # bitrate
                0,  # kf_mode
                0,  # kf_min_dist
                173,  # kf_max_dist
                ]
    elif resolution == 'WXGA':
        return [243,  # gop
                0,  # drop_frame
                1,  # resize_allowed
                73,  # resize_up
                28,  # resize_down
                20,  # undershoot_pct
                0,  # overshoot_pct
                26,  # min_q
                0,  # end_usage
                0,  # buffer_size
                0,  # buffer_init_size
                3275, # buffer_optimal_size
                3559766,  # bitrate
                1,  # kf_mode
                0,  # kf_min_dist
                0,  # kf_max_dist
                ]
    elif resolution == 'KITTY':
        return [250,  # gop
                0,  # drop_frame
                0,  # resize_allowed
                100,  # resize_up
                100,  # resize_down
                100,  # undershoot_pct
                0,  # overshoot_pct
                41,  # min_q
                1,  # end_usage
                6000,  # buffer_size
                444,  # buffer_init_size
                3547, # buffer_optimal_size
                5000000,  # bitrate
                0,  # kf_mode
                0,  # kf_min_dist
                250,  # kf_max_dist
                ]
    elif resolution == 'FHD':
        return [250,  # gop
                0,  # drop_frame
                0,  # resize_allowed
                100,  # resize_up
                100,  # resize_down
                100,  # undershoot_pct
                0,  # overshoot_pct
                41,  # min_q
                1,  # end_usage
                6000,  # buffer_size
                444,  # buffer_init_size
                3547, # buffer_optimal_size
                5000000,  # bitrate
                0,  # kf_mode
                0,  # kf_min_dist
                250,  # kf_max_dist
                ]
    elif resolution == 'QXGA':
        return [250,  # gop
                0,  # drop_frame
                0,  # resize_allowed
                100,  # resize_up
                100,  # resize_down
                100,  # undershoot_pct
                0,  # overshoot_pct
                41,  # min_q
                1,  # end_usage
                6000,  # buffer_size
                444,  # buffer_init_size
                3547, # buffer_optimal_size
                5000000,  # bitrate
                0,  # kf_mode
                0,  # kf_min_dist
                250,  # kf_max_dist
                ]

@use_named_args(SPACE)
def objective(gop, drop_frame, resize_allowed, resize_up, resize_down,
              undershoot_pct, overshoot_pct, min_q, end_usage, buffer_size, buffer_init_size,
              buffer_optimal_size, bitrate, kf_mode, kf_min_dist, kf_max_dist):

    print(TAG)
    utilities.reset_time_out()  # resets violation variable

    try:  # try/catch to catch when the containers crash due to illegal parameter combination
        def get_list_encoder():
            return ['--cid=' + utilities.CID,
                    '--name=' + utilities.SHARED_MEMORY_AREA,
                    '--width=' + _local_variables['width'],
                    '--height=' + _local_variables['height'],
                    '--vp9',
                    #'--verbose',
                    ###################
                    '--gop=' + str(gop),
                    '--threads=4',
                    '--drop-frame=' + str(drop_frame),
                    '--resize-allowed=' + str(resize_allowed),
                    '--resize-up=' + str(resize_up),
                    '--resize-down=' + str(resize_down),
                    '--undershoot-pct=' + str(undershoot_pct),
                    '--overshoot-pct=' + str(overshoot_pct),
                    '--min-q=' + str(min_q),
                    '--end-usage=' + str(end_usage),
                    '--buffer-size=' + str(buffer_size),
                    '--buffer-init-size=' + str(buffer_init_size),
                    '--buffer-optimal-size=' + str(buffer_optimal_size),
                    '--bitrate=' + str(bitrate),
                    '--kf-mode=' + str(kf_mode),
                    '--kf-min-dist=' + str(kf_min_dist),
                    '--kf-max-dist=' + str(kf_max_dist)
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
        def handler(signum, frame):
            print('Signal handler called with signal', signum)
            container_ffe.kill()
            container_encoder.kill()

        # Setup alarm on threads, if the container does not terminate before 
        # the CONTAINER_THREAD_TIMEOUT a kill signal is called. 
        # Only availible on unix systems. 
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(utilities.CONTAINER_THREAD_TIME_OUT)

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
