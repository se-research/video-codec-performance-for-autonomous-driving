import docker
import threading
import sys
import os
import csv
import time
from skopt import gp_minimize
from skopt.space import Integer, Categorical
from skopt.utils import use_named_args
from skopt.plots import plot_convergence
import matplotlib.pyplot as plt
import plot_generator

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
resolution = 'not_set'

best_config = 'not_set'
config = 0
max_ssim = 0

INITIAL_WIDTH = '2048'
INITIAL_HEIGHT = '1536'

STOP_AFTER = 80
TIMED_OUT_MSG_BYTES = str.encode('[frame-feed-evaluator]: Timed out while waiting for encoded frame.\n')
TIMED_OUT = 0

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

# Returns coordinates so that the cropping will grow from the center/bottom line
def calculate_crop_x():
    return str(int(INITIAL_WIDTH) / 2 - (int(width) / 2))


def calculate_crop_y():
    return str(int(INITIAL_HEIGHT) - (int(height)))


#######################################################  FFE  ##########################################################
PNGS_PATH = os.path.join(os.getcwd(), '../2019-03-22_AstaZero_RuralRoad')
OUTPUT_REPORT_PATH = os.path.join(os.getcwd(), 'reports')
OUTPUT_GRAPH_PATH = os.path.join(os.getcwd(), 'graphs')
OUTPUT_BEST_CONFIG_REPORT_PATH = os.path.join(os.getcwd(), 'best_configs_report')

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


# Iterates the generator and prints its log and sets violation TIMED_OUT
def log_helper(log_generator, color):
    for x in log_generator:
        print('\033[' + color + 'm### \033[0m' + (str(x, 'utf-8')))  # Prints with color code prefix and in utf-8
        if x == TIMED_OUT_MSG_BYTES:
            global TIMED_OUT
            TIMED_OUT = 1


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


# https://www.web3.lu/avc-h264-video-settings/ # https://www.pixeltools.com/rate_control_paper.html
# https://superuser.com/questions/638069/what-is-the-maximum-and-minimum-of-q-value-in-ffmpeg
# https://slhck.info/video/2017/02/24/crf-guide.html
# All parameters available in h264 and their ranges
space_h264 = [Integer(100000, 1500000, name='bitrate'),
              Integer(100000, 1500000, name='bitrate_max'),
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

param_list_h264 = (
    'bitrate', 'bitrate_max', 'gop', 'rc_mode', 'ecomplexity', 'sps_pps_strategy', 'num_ref_frame', 'ssei',
    'prefix_nal', 'entropy_coding', 'frame_skip', 'qp_max', 'qp_min', 'long_term_ref', 'loop_filter', 'denoise',
    'background_detection', 'adaptive_quant', 'frame_cropping', 'scene_change_detect', 'padding'
)


@use_named_args(space_h264)
def objective_h264(bitrate, bitrate_max, gop, rc_mode, ecomplexity, sps_pps_strategy, num_ref_frame, ssei, prefix_nal,
                   entropy_coding, frame_skip, qp_max, qp_min, long_term_ref, loop_filter, denoise,
                   background_detection, adaptive_quant, frame_cropping, scene_change_detect, padding):
    # update report name with this iteration's config
    global config
    report_name = 'ffe-AstaZero_Rural_Road-' + TAG_ENCODER + '-' + res[0] + '-' + 'C' + str(config) + '.csv'
    config += 1

    global TIMED_OUT
    TIMED_OUT = 0  # resets violation variable

    def get_list_ffe():
        return ['--folder=/pngs',
                '--report=' + report_name,
                '--cid=' + CID,
                '--name=' + SHARED_MEMORY_AREA,
                '--crop.x=' + calculate_crop_x(),
                '--crop.y=' + calculate_crop_y(),
                '--crop.width=' + width,
                '--crop.height=' + height,
                '--delay=0',
                '--delay.start=150',
                '--stopafter=' + str(STOP_AFTER),
                # '--noexitontimeout'
                # '--verbose',
                ]

    def get_list_encoder():
        return ['--cid=' + CID,
                '--name=' + SHARED_MEMORY_AREA,
                '--width=' + width,
                '--height=' + height,
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
        thread_logs_ffe = threading.Thread(target=log_helper, args=[container_ffe.logs(stream=True), PREFIX_COLOR_FFE])
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


if __name__ == '__main__':
    docker_client = docker.from_env()
    main(docker_client)

    reports = []

    for (i, res) in enumerate(RESOLUTIONS):
        width = res[1]
        height = res[2]
        resolution = RESOLUTIONS[0]
        max_ssim = 0  # resets max SSIM, config and best config for current resolution
        best_config = 'not_set'
        config = 0

        start = time.time()
        minimize_results = gp_minimize(func=objective_h264, dimensions=space_h264, base_estimator=None,
                                       n_calls=100, n_random_starts=10,
                                       acq_func="gp_hedge", acq_optimizer="auto", x0=None, y0=None,
                                       random_state=None, verbose=True, callback=None,
                                       n_points=10000, n_restarts_optimizer=5, xi=0.01, kappa=1.96,
                                       noise="gaussian", n_jobs=1, )
        now = time.time()

        print("Best score=%.4f" % minimize_results.fun)
        print("Best parameters:")

        best_parameters = []
        i = 0
        for value in minimize_results.x:
            best_parameters.append(param_list_h264[i] + ': ' + str(value))
            print(param_list_h264[i] + ': ' + str(value))  # prints parameters that obtained the highest SSIM
            i += 1
        print("Best config: " + best_config)
        print("It took: ", str((now - start) / 60), " minutes")

        plot_convergence(minimize_results)
        plt.show()

        reports.append('reports/' + best_config)

        # Saves the best parameter config combo in OUTPUT_BEST_CONFIG_REPORT_PATH, creates dir if not already exists
        if os.path.isdir(OUTPUT_BEST_CONFIG_REPORT_PATH):
            best_config_file = open(OUTPUT_BEST_CONFIG_REPORT_PATH + '/' + best_config, 'w')  # opens/creates file
            best_config_file.writelines(best_parameters)
            print("Best parameters saved: " + OUTPUT_BEST_CONFIG_REPORT_PATH + '/' + best_config)
        else:
            try:
                os.mkdir(OUTPUT_BEST_CONFIG_REPORT_PATH)
                best_config_file = open(OUTPUT_BEST_CONFIG_REPORT_PATH + '/' + best_config, 'w')  # opens/creates file
                best_config_file.writelines(best_parameters)
                print("Best parameters saved: " + OUTPUT_BEST_CONFIG_REPORT_PATH + '/' + best_config)
            except Exception as e:
                print("Creation of the dir %s failed. " + e % OUTPUT_BEST_CONFIG_REPORT_PATH)

    plot_generator.run(reports, OUTPUT_GRAPH_PATH)
