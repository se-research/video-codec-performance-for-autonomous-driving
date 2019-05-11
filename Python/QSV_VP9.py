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

REPO = 'https://github.com/guslauer/video-qsv-vp9-encoder.git'
VERSION = 'latest'  # @TODO change
TAG = 'qsv-vp9:' + VERSION # @TODO change

PARAMETERS = (
    'gop', 'bitrate', 'ip-period', 'init-qp', 'qpmin', 'qpmax', 'disable-frame-skip', 'diff-qp-ip', 'diff-qp-ib',
    'num-ref-frame', 'rc-mode', 'reference-mode')


# All parameters available in qsv-h264 and their ranges
# https://github.com/intel/libyami-utils/blob/c64cad218e676cc02b426cb67b660d8eb2567d3b/tests/encodehelp.h
# https://github.com/intel/libyami/blob/apache/interface/VideoEncoderDefs.h
# https://github.com/intel/libyami-utils/blob/master/doc/yamitranscode.1
SPACE = [Integer(1, 250, name='gop'),
         Integer(100, 5000, name='bitrate'),
         Integer(0, 50, name='ip_period'),  # @TODO check range
         Integer(0, 51, name='init_qp'),
         Integer(0, 50, name='qpmin'),
         Integer(0, 51, name='qpmax'),
         Categorical((0, 1), name='disable_frame_skip'),
         Integer(0, 51, name='diff_qp_ip'),  # @TODO check range
         Integer(0, 51, name='diff_qp_ib'),  # @TODO check range
         Integer(0, 16, name='num_ref_frame'),
         Integer(0, 4, name='rc_mode'),
         Categorical((0, 1), name='reference_mode'),
         ]


def get_default_encoder_config():
    return [10,  # gop
            2000,  # bitrate
            0,  # ip-period
            26,  # init-qp
            1,  # qpmin
            51,  # qpmax
            0,  # disable-frame-skip
            0,  # diff-qp-ip
            0,  # diff-qp-ib
            1,  # num-ref-frame
            4,  # rc-mode
            0,  # reference-mode
            ]


@use_named_args(SPACE)
def objective(gop, bitrate, ip_period, init_qp, qpmin, qpmax, disable_frame_skip, diff_qp_ip, diff_qp_ib,
              num_ref_frame, rc_mode, reference_mode):

    print(TAG)
    utilities.reset_time_out()  # resets violation variable

    try:  # try/catch to catch when the containers crash due to illegal parameter combination
        def get_list_encoder():
            return ['--cid=' + utilities.CID,
                    '--name=' + utilities.SHARED_MEMORY_AREA,
                    '--width=' + _local_variables['width'],
                    '--height=' + _local_variables['height'],
                    '--gop=' + str(gop),
                    '--bitrate=' + str(bitrate),
                    '--ip-period=' + str(ip_period),
                    '--init_qp=' + str(init_qp),
                    '--qpmin=' + str(qpmin),
                    '--qpmax=' + str(qpmax),
                    '--disable-frame-skip=' + str(disable_frame_skip),
                    '--diff-qp-ip=' + str(diff_qp_ip),
                    '--diff-qp-ib=' + str(diff_qp_ib),
                    '--num-ref-frame=' + str(num_ref_frame),
                    '--rc-mode' + str(rc_mode),
                    '--reference-mode=' + str(reference_mode),
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
                                                                             devices=['/dev/dri/renderD128:/dev/dri/renderD128:rwm'],
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

    file = open(utilities.OUTPUT_REPORT_PATH + '/' + _local_variables['report_name'], 'r')  # opens report generated
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
