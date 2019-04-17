import docker
import threading
#import plot_generator
import sys
import os
import numpy as np
from evolutionary_search import maximize
import csv

REPO_FFE = 'https://github.com/chrberger/frame-feed-evaluator.git'
REPO_X264 = 'https://github.com/chalmers-revere/opendlv-video-x264-encoder.git'
REPO_H264 = 'https://github.com/chalmers-revere/opendlv-video-h264-encoder.git'
REPO_H264_FULL = 'https://github.com/guslauer/opendlv-video-h264-encoder.git'

VERSION_FFE = 'v0.0.4'
TAG_FFE = 'ffe:' + VERSION_FFE
PREFIX_COLOR_FFE = '92'

'''
VERSION_ENCODER = 'v0.0.7'
TAG_ENCODER = 'x264:' + VERSION_ENCODER
PREFIX_COLOR_ENCODER = '94'
'''
VERSION_ENCODER = 'v0.0.1'
TAG_ENCODER = 'h264:' + VERSION_ENCODER
PREFIX_COLOR_ENCODER = '94'

'''
VERSION_ENCODER = 'latest'
TAG_ENCODER = 'h264-full:' + VERSION_ENCODER
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

######################
# https://www.web3.lu/avc-h264-video-settings/ # https://www.pixeltools.com/rate_control_paper.html
# https://superuser.com/questions/638069/what-is-the-maximum-and-minimum-of-q-value-in-ffmpeg
# https://slhck.info/video/2017/02/24/crf-guide.html

rc_mode = 0  # -1 -3
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
#bitrate = 100000  # 100,000 - 5,000,000
gop = 1


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


def get_list_encoder_h264_full():
    return ['--cid=' + CID,
            '--name=' + SHARED_MEMORY_AREA,
            '--width=' + width,
            '--height=' + height,
            # '--verbose,',
            ###################
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
            '--bitrate=' + str(bitrate)
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

def f(bitrate):
    print('SET BITRATE FROM GA: ' + str(bitrate))
    def get_list_ffe():
        return ['--folder=/pngs',
                '--report=' + str(bitrate) +'.csv',
                '--cid=' + CID,
                '--name=' + SHARED_MEMORY_AREA,
                '--crop.x=' + calculate_crop_x(),
                '--crop.y=' + calculate_crop_y(),
                '--crop.width=' + width,
                '--crop.height=' + height,
                '--noexitontimeout',
                '--delay=0',
                '--delay.start=1000',
                '--stopafter=15',
                #'--verbose',
                ]

    def get_list_encoder():
        return ['--cid=' + CID,
                '--name=' + SHARED_MEMORY_AREA,
                '--width=' + width,
                '--height=' + height,
                '--bitrate=' + str(bitrate),
                #'--verbose'
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
    avg = sum / length
    print(avg)
    return avg


if __name__ == '__main__':
    docker_client = docker.from_env()
    main(docker_client)

    paramgrid = {"bitrate": np.arange(100000, 1500000, 100000)}
    best_params, best_ssim, score_results, _, _ = maximize(func=f, parameter_dict=paramgrid, verbose=False,
                                                           population_size=5, tournament_size=2, generations_number=3)

    print(best_params)
    #print(best_ssim)
    print(score_results)
