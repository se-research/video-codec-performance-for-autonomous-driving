import docker
import threading
import time
import plot_generator

REPO_FFE = 'https://github.com/chrberger/frame-feed-evaluator.git'
REPO_X264 = 'https://github.com/chalmers-revere/opendlv-video-x264-encoder.git'
REPO_H264 = 'https://github.com/chalmers-revere/opendlv-video-h264-encoder.git'

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

width = '640'
height = '480'

INITIAL_WIDTH = '2048'
INITIAL_HEIGHT = '1536'

CID = '112'
SHARED_MEMORY_AREA = 'video1'
report_name = 'ffe-AstaZero_Rural_Road-h264-VGA-C1.csv'

RESOLUTIONS = [['VGA', '640', '480'], ['SVGA', '800', '600'], ['XGA', '1024', '768'], ['HD720', '1280', '720'],
               ['HD1080', '1920', '1080'], ['QXGA', '2048', '1536']]


# Returns coordinates so that the cropping will grow from the center/bottom line
def calculate_crop_x():
    return str(int(INITIAL_WIDTH) / 2 - (int(width) / 2))


def calculate_crop_y():
    return str(int(INITIAL_HEIGHT) - (int(height)))


#######################################################  FFE  ##########################################################

PNGS_PATH = '/home/erik/Desktop/Thesis/video-codec-performance-for-autonomous-driving/2019-03-22_AstaZero_RuralRoad/'
REPORT_PATH = '/home/erik/Desktop/coordinator/video-codec-eval-coordinator/reports'
GRAPH_PATH = '/home/erik/Desktop/coordinator/video-codec-eval-coordinator/graphs'

VOLUMES_FFE = {'/tmp/': {'bind': '/tmp', 'mode': 'rw'},
               REPORT_PATH: {'bind': '/host', 'mode': 'rw'},
               PNGS_PATH: {
                   'bind': '/pngs',
                   'mode': 'rw'}
               }


def get_list_ffe():
    return ["--folder=/pngs",
            "--report=" + report_name,
            "--cid=" + CID,
            "--name=" + SHARED_MEMORY_AREA,
            "--crop.x=" + calculate_crop_x(),
            "--crop.y=" + calculate_crop_y(),
            "--crop.width=" + width,
            "--crop.height=" + height,
            # "--verbose",
            '--noexitontimeout',
            '--delay=0'
            ]


#####################################################  ENCODER  ########################################################
def get_list_encoder():
    return ["--cid=" + CID,
            "--name=" + SHARED_MEMORY_AREA,
            "--width=" + width,
            "--height=" + height,
            "--bitrate=100000",
            "--verbose"]


########################################################################################################################

# Iterates the generator and prints its log
def print_logs(log_generator, color):
    for x in log_generator:
        print('\033[' + color + 'm### \033[0m' + (str(x, 'utf-8')))  # Prints with color code prefix and in utf-8


client = docker.from_env()


def build_ffe():
    try:
        client.images.get(TAG_FFE)
        print('Found ' + TAG_FFE + ' image locally')
    except docker.errors.ImageNotFound:
        print('Building ' + TAG_FFE + ' from ' + REPO_FFE + '#' + VERSION_ENCODER + '. It may take some time...')
        image = client.images.build(path=REPO_FFE + '#' + VERSION_FFE,
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
        client.images.get(TAG_ENCODER)
        print('Found ' + TAG_ENCODER + ' image locally')
    except docker.errors.ImageNotFound:
        print('Building ' + TAG_ENCODER + ' from ' + REPO_H264 + '#' + VERSION_ENCODER + '. It may take some time...')
        image = client.images.build(path=REPO_H264 + '#' + VERSION_ENCODER,
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

reports = []
for (i, res) in enumerate(RESOLUTIONS):
    report_name = 'ffe-AstaZero_Rural_Road-h264-' + res[0] + '-C1.csv'
    reports.append('reports/' + report_name)
    width = res[1]
    height = res[2]

    print(get_list_ffe())
    print(get_list_encoder())

    container_ffe = client.containers.run(TAG_FFE,
                                          command=get_list_ffe(),
                                          volumes=VOLUMES_FFE,
                                          environment=['DISPLAY=:0'],
                                          working_dir='/host',
                                          network_mode="host",
                                          ipc_mode="host",
                                          remove=True,
                                          detach=True,
                                          )

    container_encoder = client.containers.run(TAG_ENCODER,
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

reports = []
for (i, res) in enumerate(RESOLUTIONS):
    report_name = 'ffe-AstaZero_Rural_Road-h264-' + res[0] + '-C1.csv'
    reports.append('reports/' + report_name)

plot_generator.run(reports, GRAPH_PATH)
