import docker
import threading
import sys
import os
import csv
import time
from skopt import gp_minimize
from skopt.space import Integer
from skopt.utils import use_named_args
import matplotlib.pyplot as plt

REPO_FFE = 'https://github.com/chrberger/frame-feed-evaluator.git'
REPO_X264_FULL = 'https://github.com/guslauer/opendlv-video-x264-encoder.git'
REPO_H264 = 'https://github.com/chalmers-revere/opendlv-video-h264-encoder.git'
REPO_VPX_FULL = 'https://github.com/jeberlen/opendlv-video-vpx-encoder.git'

VERSION_FFE = 'v0.0.4'
TAG_FFE = 'ffe:' + VERSION_FFE
PREFIX_COLOR_FFE = '92'

VERSION_ENCODER = 'v0.0.2'
TAG_ENCODER = 'h264:' + VERSION_ENCODER
PREFIX_COLOR_ENCODER = '94'

'''
VERSION_ENCODER = 'v0.0.7'
TAG_ENCODER = 'x264:' + VERSION_ENCODER
PREFIX_COLOR_ENCODER = '94'

VERSION_ENCODER = 'v0.0.7'
TAG_ENCODER = 'x264-full:' + VERSION_ENCODER
PREFIX_COLOR_ENCODER = '94'


VERSION_ENCODER = 'latest'
TAG_ENCODER = 'vpx-full:' + VERSION_ENCODER
PREFIX_COLOR_ENCODER = '94'
'''

width = '640'
height = '480'

report_name = 'test'

INITIAL_WIDTH = '2048'
INITIAL_HEIGHT = '1536'

CID = '112'
SHARED_MEMORY_AREA = 'video1'

RESOLUTIONS = [['VGA', '640', '480'], ['SVGA', '800', '600'], ['XGA', '1024', '768'], ['HD720', '1280', '720'],
               ['HD1080', '1920', '1080'], ['QXGA', '2048', '1536']]

#####################
# http://doxygen.db48x.net/mozilla/html/structvpx__codec__enc__cfg.html
# Parameters according to https://www.webmproject.org/docs/encoder-parameters/

# gop = 1 # 1 - n of frames

g_timebase_num = 1  # Unsure if we need to change
g_timebase_den = 20  # Unsure if we need to change
g_threads = 1  # 1 - 4
g_profile = 0  # 0 - 1
g_lag_in_frames = 0  # 0 - 25 (over 12 turns on alt-ref frame, a VPx quality enhancer)

rc_dropframe_thresh = 0.0  # 0.0 - 1.0
rc_resize_allowed = 0  # 0 - 1
rc_resize_up_thresh = 0.0  # 0.0 - 1.0
rc_resize_down_thresh = 0.0  # 0.0 - 1.0
rc_undershoot_pct = 0  # 0 - 100 | VP8 ? 0 - 1000
rc_overshoot_pct = 0  # 0 - 100 | VP8 ? 0 - 1000
rc_min_quantizer = 0  # 0 - 52 | VP8 ? 0 - 56
rc_max_quantizer = 0  # 0 - 52 | VP8 ? 0 - 56
rc_end_usage = 0  # 0 - 1
rc_buf_sz = 0  # 0 - 60000
rc_buf_initial_sz = 0  # 0 - 40000
rc_buf_optimal_sz = 0  # 0 - 50000
rc_target_bitrate = 100000  # 100000 - 5000000

kf_mode = 0  # 0 - 1
kf_min_dist = 0  # 0 - n of frames
kf_max_dist = 0  # 0 - n of frames

######################
# https://www.web3.lu/avc-h264-video-settings/ # https://www.pixeltools.com/rate_control_paper.html
# https://superuser.com/questions/638069/what-is-the-maximum-and-minimum-of-q-value-in-ffmpeg
# https://slhck.info/video/2017/02/24/crf-guide.html

# rc_mode = 0  # -1 - 3
ecomplexity = 0  # 0 - 2
num_ref_frame = 1  # 1 - 16
sps_pps_strategy = 0  # 0, 1, 2, 3, 6
b_prefix_nal = 0  # 0, 1
b_ssei = 0  # 0, 1
i_padding = 0  # 0, 1
i_entropy_coding = 0  # 0, 1
b_frame_skip = 0  # 0, 1
i_bitrate_max = 5000000  # -5,000,000
i_max_qp = 51  # 0 - 51 def: 42 // reasonable: 32 - 51?
i_min_qp = 18  # 0 - 50 def: 12 // reasonable: 7 - 17?
i_long_term_reference = 0  # 0, 1
i_loop_filter = 0  # 0, 1, 2
b_denoise = 0  # 0, 1
b_background_detection = 0  # 0, 1
b_adaptive_quant = 0  # 0, 1
b_frame_cropping = 0  # 0, 1
b_scene_change_detect = 0  # 0, 1


# bitrate = 100000  # 100,000 - 5,000,000
# gop = 1


######################

# Returns coordinates so that the cropping will grow from the center/bottom line
def calculate_crop_x():
    return str(int(INITIAL_WIDTH) / 2 - (int(width) / 2))


def calculate_crop_y():
    return str(int(INITIAL_HEIGHT) - (int(height)))


#######################################################  FFE  ##########################################################
PNGS_PATH = os.path.join(os.getcwd(), '../2019-03-22_AstaZero_RuralRoad')
OUTPUT_REPORT_PATH = os.path.join(os.getcwd(), 'reports')
OUTPUT_GRAPH_PATH = os.path.join(os.getcwd(), 'graphs')

VOLUMES_FFE = {'/tmp/': {'bind': '/tmp', 'mode': 'rw'},
               OUTPUT_REPORT_PATH: {'bind': '/host', 'mode': 'rw'},
               PNGS_PATH: {
                   'bind': '/pngs',
                   'mode': 'rw'}
               }


def get_list_encoder_vp9_full():
    return ['--cid=' + CID,
            '--name=' + SHARED_MEMORY_AREA,
            '--width=' + width,
            '--height=' + height,
            # '--verbose',
            ###################
            '--gop=' + str(gop),
            '--threads=' + str(g_threads),
            '--profile=' + str(g_profile),
            '--lag-in-frame=' + str(g_lag_in_frames),
            '--drop-frame=' + str(rc_dropframe_thresh),
            '--resize-allowed=' + str(rc_resize_allowed),
            '--resize-up=' + str(rc_resize_up_thresh),
            '--resize-down=' + str(rc_resize_down_thresh),
            '--undershoot-pct=' + str(rc_undershoot_pct),
            '--overshoot-pct=' + str(rc_overshoot_pct),
            '--min-q=' + str(rc_min_quantizer),
            '--max-q=' + str(rc_max_quantizer),
            '--end-usage=' + str(rc_end_usage),
            '--buffer-size=' + str(rc_buf_sz),
            '--buffer-init-size=' + str(rc_buf_initial_sz),
            '--buffer-optimal-size=' + str(rc_buf_optimal_sz),
            '--bitrate=' + str(rc_target_bitrate),
            '--kf-mode=' + str(kf_mode),
            '--kf-min-dist=' + str(kf_min_dist),
            '--kf-max-dist=' + str(kf_max_dist)
            ]


def get_list_encoder_h264_full():
    return ['--cid=' + CID,
            '--name=' + SHARED_MEMORY_AREA,
            '--width=' + width,
            '--height=' + height,
            # '--verbose,',
            ###################

            '--bitrate=' + str(bitrate),
            '--bitrate=' + str(bitrate),

            '--rc-mode=' + str(rc_mode),
            '--ecomplexity=' + str(ecomplexity),
            '--num-ref-frame=' + str(num_ref_frame),
            '--sps-pps=' + str(sps_pps_strategy),
            '--prefix-nal=' + str(b_prefix_nal),
            '--ssei=' + str(b_ssei),
            '--padding=' + str(i_padding),
            '--entropy-coding=' + str(i_entropy_coding),
            '--frame-skip=' + str(b_frame_skip),
            '--bitrate-max=' + str(i_bitrate_max),
            '--qp-max=' + str(i_max_qp),
            '--qp-min=' + str(i_min_qp),
            '--long-term-ref=' + str(i_long_term_reference),
            '--loop-filter=' + str(i_loop_filter),
            '--denoise=' + str(b_denoise),
            '--background-detection=' + str(b_background_detection),
            '--adaptive-quant=' + str(b_adaptive_quant),
            '--frame-cropping=' + str(b_frame_cropping),
            '--scene-change-detect=' + str(b_scene_change_detect),
            '--gop=' + str(gop),
            ]


# Iterates the generator and prints its log
def print_logs(log_generator, color):
    for x in log_generator:
        print('\033[' + color + 'm### \033[0m' + (str(x, 'utf-8')))  # Prints with color code prefix and in utf-8


########################################################################################################################


def main(docker_client):
    def build_ffe():
        try:
            docker_client.images.get(TAG_FFE)
            print('Found ' + TAG_FFE + ' image locally')
        except docker.errors.ImageNotFound:
            print('Building ' + TAG_FFE + ' from ' + REPO_FFE + '#' + VERSION_ENCODER + '. It may take some time...')
            image = docker_client.images.build(path=REPO_FFE + '#' + VERSION_FFE,
                                               dockerfile='Dockerfile.amd64',
                                               tag=TAG_FFE,
                                               rm=True,
                                               forcerm=True
                                               )
            # @TODO     docker image prune --filter label=stage=intermediate    to remove intermediate builder image
            for x in image[1]:
                print(x)
        except Exception as e:
            sys.exit(e)  # Exits script in case of failure to retrieve image

    def build_encoder():
        try:
            docker_client.images.get(TAG_ENCODER)
            print('Found ' + TAG_ENCODER + ' image locally')
        except docker.errors.ImageNotFound:
            print(
                'Building ' + TAG_ENCODER + ' from ' + REPO_H264 + '#' + VERSION_ENCODER + '. It may take some time...')
            image = docker_client.images.build(path=REPO_H264 + '#' + VERSION_ENCODER,
                                               dockerfile='Dockerfile.amd64',
                                               tag=TAG_ENCODER,
                                               rm=True,
                                               forcerm=True
                                               )
            # @TODO     docker image prune --filter label=stage=intermediate    to remove intermediate builder image
            for x in image[1]:
                print(x)
        except Exception as e:
            sys.exit(e)

    thread_build_ffe = threading.Thread(target=build_ffe)
    thread_build_encoder = threading.Thread(target=build_encoder)

    thread_build_ffe.start()
    thread_build_encoder.start()

    thread_build_ffe.join()  # Blocks execution until both threads has terminated
    thread_build_encoder.join()

    # reports = []
    # for (i, res) in enumerate(RESOLUTIONS):
    #     report_name = 'ffe-AstaZero_Rural_Road-' + TAG_ENCODER + '-' + res[0] + '-  .csv'
    #     reports.append('reports/' + report_name)
    #     width = res[1]
    #     height = res[2]
    #
    #     print(get_list_ffe())
    #     print(get_list_encoder())


#    plot_generator.run(reports, OUTPUT_GRAPH_PATH)

param_grid0 = [Integer(100000, 1500000, name='bitrate'),
               Integer(0, 1, name='entropy_coding'),
               Integer(0, 1, name='denoise'),
               Integer(0, 2, name='ecomplexity'),
               Integer(0, 1, name='adaptive_quant')
               ]


@use_named_args(param_grid0)
def f(bitrate, denoise, entropy_coding, adaptive_quant, ecomplexity):
    # print('bitrate: ' + str(bitrate))# + '\ndenoise: ' + str(denoise) +'\nentropy_coding: ' + str(entropy_coding))

    def get_list_ffe():
        return ['--folder=/pngs',
                '--report=' + str(bitrate) + '.csv',
                '--cid=' + CID,
                '--name=' + SHARED_MEMORY_AREA,
                '--crop.x=' + calculate_crop_x(),
                '--crop.y=' + calculate_crop_y(),
                '--crop.width=' + width,
                '--crop.height=' + height,
                '--delay=0',
                '--delay.start=150',
                '--stopafter=40',
                #'--noexitontimeout'
                #'--verbose',
                '--timeout=100'
                ]

    def get_list_encoder():
        return ['--cid=' + CID,
                '--name=' + SHARED_MEMORY_AREA,
                '--width=' + width,
                '--height=' + height,
                '--rc-mode=1',
                '--bitrate=' + str(bitrate),
                '--denoise' + str(denoise),
                '--entropy-coding' + str(entropy_coding),
                '--adaptive_quant' + str(adaptive_quant),
                '--ecomplexity' + str(ecomplexity),
               # '--verbose'
                ]

    container_ffe = docker_client.containers.run(TAG_FFE,
                                                 command=get_list_ffe(),
                                                 volumes=VOLUMES_FFE,
                                                 environment=['DISPLAY=:0'],
                                                 working_dir='/host',
                                                 network_mode="host",
                                                 ipc_mode="host",
                                                 remove=True,
                                                 detach=True,
                                                 )

    container_encoder = docker_client.containers.run(TAG_ENCODER,
                                                     command=get_list_encoder(),
                                                     volumes={'/tmp': {'bind': '/tmp', 'mode': 'rw'}},
                                                     network_mode="host",
                                                     ipc_mode="host",
                                                     remove=True,
                                                     detach=True
                                                     )

    thread_logs_ffe = threading.Thread(target=print_logs, args=[container_ffe.logs(stream=True), PREFIX_COLOR_FFE])
    thread_logs_encoder = threading.Thread(target=print_logs, args=[container_encoder.logs(stream=True),
                                                                    PREFIX_COLOR_ENCODER])

    thread_logs_ffe.start()
    thread_logs_encoder.start()

    thread_logs_ffe.join()  # @TODO  Change to have the actual containers, encoder and ffe, blocking
    thread_logs_encoder.join()

    file = open(OUTPUT_REPORT_PATH + '/' + str(bitrate) + '.csv', 'r')
    plots = csv.reader(file, delimiter=';')
    sum = 0
    length = 0
    for row in plots:
        sum += float(row[10])
        length += 1

    if length < 15:
        print("length only :" + str(length))
        return 1
    avg = sum / length
    return 1 - avg


if __name__ == '__main__':
    docker_client = docker.from_env()
    main(docker_client)

    start0 = time.time()

    res = gp_minimize(func=f, dimensions=param_grid0, base_estimator=None,
                      n_calls=10, n_random_starts=10,
                      acq_func="gp_hedge", acq_optimizer="auto", x0=None, y0=None,
                      random_state=None, verbose=True, callback=None,
                      n_points=10000, n_restarts_optimizer=5, xi=0.01, kappa=1.96,
                      noise="gaussian", n_jobs=1, )
    now0 = time.time()

    print("----------minimize-----------")
    print("Best score=%.4f" % res.fun)
    print("""Best parameters:
    - bitrate: %d
    - entropy_coding: %d
    - denoise: %d
    - ecomplexity: %d
    - adaptive_quant: %d"""
          % (res.x[0], res.x[1], res.x[2], res.x[3], res.x[4]))

    from skopt.plots import plot_convergence

    plot_convergence(res)
    plt.show()

    print("It took: ", now0 - start0, " seconds")
    print("Or : ", (now0 - start0) / 60, " minutes")
