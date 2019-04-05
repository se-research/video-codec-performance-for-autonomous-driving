import docker
import threading

REPO_FFE = 'https://github.com/chrberger/frame-feed-evaluator.git'
REPO_X264 = 'https://github.com/chalmers-revere/opendlv-video-x264-encoder.git'

VERSION_FFE = 'v0.0.4'
TAG_FFE = 'ffe:' + VERSION_FFE
PREFIX_COLOR_FFE = '92'

VERSION_ENCODER = 'v0.0.7'
TAG_ENCODER = 'x264:' + VERSION_ENCODER
PREFIX_COLOR_ENCODER = '94'

PNGS_PATH = '/home/erik/Desktop/Thesis/video-codec-performance-for-autonomous-driving/2019-03-22_AstaZero_RuralRoad/'
REPORT_PATH = '/home/erik/Desktop/coordinator'

VOLUMES_FFE = {'/tmp/': {'bind': '/tmp', 'mode': 'rw'},
               REPORT_PATH: {'bind': '/host', 'mode': 'rw'},
               PNGS_PATH: {
                   'bind': '/pngs',
                   'mode': 'rw'}
               }

COMMAND_LIST_FFE = ["--folder=/pngs",
                    "--report=ffe-x264-python.csv",
                    "--cid=112",
                    "--name=video1",
                    "--crop.x=376",
                    "--crop.y=32",
                    "--crop.width=640",
                    "--crop.height=480",
                    "--verbose",
                    '--noexitontimeout'
                    ]

COMMAND_LIST_ENCODER = ["--cid=112",
                        "--name=video1",
                        "--width=640",
                        "--height=480",
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
        print('Building ' + TAG_ENCODER + ' from ' + REPO_X264 + '#' + VERSION_ENCODER + '. It may take some time...')
        image = client.images.build(path=REPO_X264 + '#' + VERSION_ENCODER,
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

container_ffe = client.containers.run(TAG_FFE,
                                      command=COMMAND_LIST_FFE,
                                      volumes=VOLUMES_FFE,
                                      environment=['DISPLAY=:0'],
                                      working_dir='/host',
                                      network_mode="host",
                                      ipc_mode="host",
                                      remove=True,
                                      detach=True,
                                      )

container_encoder = client.containers.run(TAG_ENCODER,
                                          command=COMMAND_LIST_ENCODER,
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

