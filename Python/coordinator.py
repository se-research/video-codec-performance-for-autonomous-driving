import docker
import threading
import sys
import os
import time
from skopt import gp_minimize
from skopt.plots import plot_convergence
import matplotlib.pyplot as plt
import plot_generator
import utilities
import H264
import FFE

REPO_X264_FULL = 'https://github.com/guslauer/opendlv-video-x264-encoder.git'
REPO_VPX_FULL = 'https://github.com/jeberlen/opendlv-video-vpx-encoder.git'

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

INITIAL_WIDTH = '2048'
INITIAL_HEIGHT = '1536'

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

#######################################################  FFE  ##########################################################

OUTPUT_GRAPH_PATH = os.path.join(os.getcwd(), 'graphs')
OUTPUT_BEST_CONFIG_REPORT_PATH = os.path.join(os.getcwd(), 'best_configs_report')

"""
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
"""


def build(docker_client, encoder):
    def build_ffe():
        try:
            docker_client.images.get(FFE.TAG)
            print('Found ' + FFE.TAG + ' image locally')
        except docker.errors.ImageNotFound:
            print(
                'Building ' + FFE.TAG + ' from ' + FFE.REPO + '#' + FFE.VERSION + '. It may take some time...')
            image = docker_client.images.build(path=FFE.REPO + '#' + FFE.VERSION,
                                               dockerfile='Dockerfile.amd64',
                                               tag=FFE.TAG,
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
            docker_client.images.get(encoder['TAG'])
            print('Found ' + encoder['TAG'] + ' image locally')
        except docker.errors.ImageNotFound:
            print(
                'Building ' + encoder['TAG'] + ' from ' + encoder['REPO'] + '#' + encoder['VERSION'] + '. It may take some time...')
            image = docker_client.images.build(path=encoder['REPO'] + '#' + encoder['VERSION'],
                                               dockerfile='Dockerfile.amd64',
                                               tag=encoder['TAG'],
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


if __name__ == '__main__':
    docker_client = docker.from_env()

    encoders = [H264] #x264, VPX]

    for encoder in encoders:
        build(docker_client, {'TAG': encoder.TAG, 'REPO': encoder.REPO, 'VERSION': encoder.VERSION})

        reports = []
        for (i, res) in enumerate(RESOLUTIONS):
            resolution_name = res[0]
            width = res[1]
            height = res[2]
            resolution = RESOLUTIONS[0]

            report_name = utilities.generate_report_name(tag = encoder.TAG, resolution_name = resolution_name, config = config)
            config += 1
            
            encoder.initialize(init_width=INITIAL_WIDTH, init_height=INITIAL_HEIGHT, resolution=res, config=config,
                            docker_client=docker_client, report_name = report_name)
            FFE.initialize(init_width=INITIAL_WIDTH, init_height=INITIAL_HEIGHT, width=width, height=height, report_name=report_name)

            start = time.time()
            minimize_results = gp_minimize(func=encoder.objective,
                                           dimensions=encoder.SPACE,
                                           base_estimator=None,
                                           n_calls=10,
                                           n_random_starts=10,
                                           acq_func="gp_hedge",
                                           acq_optimizer="auto",
                                           x0=None,
                                           y0=None,
                                           random_state=None,
                                           verbose=True,
                                           callback=None,
                                           n_points=10000,
                                           n_restarts_optimizer=5,
                                           xi=0.01,
                                           kappa=1.96,
                                           noise="gaussian",
                                           n_jobs=1,
                                           )

            now = time.time()

            print("Best score=%.4f" % minimize_results.fun)
            print("Best parameters:")

            best_parameters = []
            i = 0
            for value in minimize_results.x:
                best_parameters.append(encoder.PARAMETERS[i] + ': ' + str(value) + '\n')
                print(encoder.PARAMETERS[i] + ': ' + str(value))  # prints parameters that obtained the highest SSIM
                i += 1
            print("Best config: " + best_config)
            print("It took: ", str((now - start) / 60), " minutes")

            ax = plot_convergence(minimize_results)
            ax.set_ylim(top=1, bottom=0)
            ax.set_title('AstaZero_Rural_Road-' + encoder.TAG + '-' + res[0])


            OUTPUT_CONVERGENCE_PATH = os.path.join(os.getcwd(), 'convergence')
            if os.path.isdir(OUTPUT_CONVERGENCE_PATH):
                plt.savefig(
                    OUTPUT_CONVERGENCE_PATH + '/' + 'AstaZero_Rural_Road-' + encoder.TAG + '-' + resolution_name + '.png')
            else:
                try:
                    os.mkdir(OUTPUT_CONVERGENCE_PATH)
                    plt.savefig(
                        OUTPUT_CONVERGENCE_PATH + '/' + 'AstaZero_Rural_Road-' + encoder.TAG + '-' + resolution_name + '.png')
                except Exception as e:
                    print(
                        "Creation of the dir %s failed. Saving graph in the same folder as the script. " + e % OUTPUT_CONVERGENCE_PATH)
                    plt.savefig(
                        OUTPUT_CONVERGENCE_PATH + '/' + 'AstaZero_Rural_Road-' + encoder.TAG + '-' + resolution_name + '.png')

            plt.clf()

            reports.append('reports/' + best_config)

            utilities.save_list(best_parameters, OUTPUT_BEST_CONFIG_REPORT_PATH, best_config)

        plot_generator.run(reports, OUTPUT_GRAPH_PATH)
