 
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

# Github repository, release version, and Docker tag
REPO = 'https://github.com/chalmers-revere/opendlv-video-vpx-encoder.git'
VERSION = 'v0.0.8'
TAG = 'vp9:' + VERSION

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
    'gop', 'drop_frame', 'resize_allowed', 'resize_up', 'resize_down',
    'undershoot_pct', 'overshoot_pct', 'min_q', 'end_usage', 'buffer_size', 'buffer_init_size', 'buffer_optimal_size', 'bitrate',
    'kf_mode', 'kf_min_dist', 'kf_max_dist', 'cpu_used'
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
         Integer(0, 250, name='kf_max_dist'),
         Integer(0, 16, name='cpu_used')
         ]


@use_named_args(SPACE)
def objective(gop, drop_frame, resize_allowed, resize_up, resize_down,
              undershoot_pct, overshoot_pct, min_q, end_usage, buffer_size, buffer_init_size,
              buffer_optimal_size, bitrate, kf_mode, kf_min_dist, kf_max_dist, cpu_used):

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
                    '--kf-max-dist=' + str(kf_max_dist),
                    '--cpu-used=' + str(cpu_used)
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
        # get_system_timeout a kill signal is called.
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

    time_violations = []
    ssim = []
    for row in report_file:
        ssim.append(float(row[10]))  # Accomulate values in SSIM column in csv
        time = float(row[12])  # Extract compression time from csv

        if time > 40000:  # If compression time is more than the allowed 40 ms
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

    return 1 - ssim_mean  # Subtract mean SSIM from 1 since the algorithm tries to find the minimum
