from skopt.space import Integer, Categorical, Real
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


REPO = 'https://github.com/guslauer/opendlv-video-x264-encoder.git'
VERSION = 'v0.0.7'  # @TODO change
TAG = 'x264:' + VERSION  # @TODO change

PARAMETERS = (
    'gop', 'preset', 'tune', 'scenecut', 'intra-refresh', 'bframe', 'badapt', 'cabac', 'rc-mode', 'qp', 'qpmin',
    'qpmax', 'qpstep', 'bitrate', 'crf', 'ipratio', 'pbratio', 'aq-mode', 'aq-strength', 'weightp', 'me', 'merange',
    'subme', 'trellis', 'nr'
)

# http://www.chaneru.com/Roku/HLS/X264_Settings.htm
# https://code.videolan.org/videolan/x264/blob/master/x264.h
# All parameters available in x264 and their ranges

SPACE = [Integer(1, 250, name='gop'),
         Categorical(('ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'),
                     name='preset'),
         Categorical(('film', 'animation', 'grain', 'stillimage', 'psnr', 'ssim', 'fastdecode', 'zerolatency'),
                     name='tune'),
         Integer(0, 100, name='scenecut'),
         Categorical((0, 1), name='intra_refresh'),
         Integer(1, 10, name='bframe'),  # @TODO check range
         Categorical((0, 1, 2), name='badapt'),
         Categorical((0, 1), name='cabac'),
         Categorical((0, 1, 2), name='rc_mode'),
         Integer(0, 51, name='qp'),
         Integer(0, 50, name='qpmin'),
         Integer(1, 51, name='qpmax'),
         Integer(1, 10, name='qpstep'),  # @TODO check range
         Integer(100000, 5000000, name='bitrate'),
         Real(13, 33, name='crf'),  # @TODO check range
         Real(1, 2, name='ipratio'),  # @TODO check range
         Real(1, 2, name='pbratio'),  # @TODO check range
         Categorical((0, 1, 2), name='aq_mode'),
         Real(0.1, 1.9, name='aq_strength'),  # @TODO check range
         Categorical((0, 1, 2,), name='weightp'),
         Integer(0, 4, name='me'),
         Integer(4, 16, name='merange'),
         Integer(2, 9, name='subme'),
         Categorical((0, 1, 2), name='trellis'),
         Integer(0, 1000, name='nr')
         ]


def get_default_encoder_config():
    return [10,  # gop
            'veryfast',  # preset
            'zerolatency',  # tune
            40,  # scenecut
            0,  # intra_refresh
            3,  # bframe
            1,  # badapt
            0,  # cabac
            1,  # rc_mode
            23,  # qp
            0,  # qpmin
            51,  # qpmax
            4,  # qpstep
            1500000,  # bitrate
            23.0,  # crf
            1.4,  # ipratio
            1.3,  # pbratio
            1,  # aq_mode
            1.0,  # aq_strength
            2,  # weightp
            1,  # me
            16,  # merange
            7,  # subme
            1,  # trellis
            0,  # nr
            ]

@use_named_args(SPACE)
def objective(gop, preset, tune, scenecut, intra_refresh, bframe, badapt, cabac, rc_mode, qp, qpmin,
    qpmax, qpstep, bitrate, crf, ipratio, pbratio, aq_mode, aq_strength, weightp, me, merange,
    subme, trellis, nr):

    print(TAG)
    utilities.reset_time_out()  # resets violation variable

    try:  # try/catch to catch when the containers crash due to illegal parameter combination
        def get_list_encoder():
            return ['--cid=' + utilities.CID,
                    '--name=' + utilities.SHARED_MEMORY_AREA,
                    '--width=' + _local_variables['width'],
                    '--height=' + _local_variables['height'],
                    '--gop=' + str(gop),
                    '--preset=' + str(preset),
                    '--tune=' + str(tune),
                    '--scenecut=' + str(scenecut),
                    '--intra-refresh=' + str(intra_refresh),
                    '--bframe=' + str(bframe),
                    '--badapt=' + str(badapt),
                    '--cabac=' + str(cabac),
                    '--rc-mode=' + str(rc_mode),
                    '--qp' + str(qp),
                    '--qpmin=' + str(qpmin),
                    '--qpmax=' + str(qpmax),
                    '--qpstep=' + str(qpstep),
                    '--bitrate' + str(bitrate),
                    '--crf=' + str(crf),
                    '--ipratio' + str(ipratio),
                    '--pbratio=' + str(pbratio),
                    '--aq-mode' + str(aq_mode),
                    '--aq-strength' + str(aq_strength),
                    '--weightp=' + str(weightp),
                    '--me=' + str(me),
                    '--merange=' + str(merange),
                    '--subme=' + str(subme),
                    '--trellis=' + str(trellis),
                    '--nr=' + str(nr),
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

    file = open(utilities.get_output_report_path()+ '/' + _local_variables['report_name'], 'r')  # opens report generated
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
