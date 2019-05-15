import os
import matplotlib.pyplot as plt
import socket
from datetime import datetime
from math import ceil

CID = '112'
SHARED_MEMORY_AREA = 'video1'

STOP_AFTER = 80
TIMED_OUT_MSG_BYTES = str.encode('[frame-feed-evaluator]: Timed out while waiting for encoded frame.\n')
TIMED_OUT = False

system_timeout = 0
DELAY_START = 300
TIMEOUT = 60
START_UP = 30
MAX_DROPPED_FRAMES = 0.95 # in %

pngs_path = 'not_set'
dataset = 'not_set'

DATASETS_PATH = os.path.join(os.getcwd(), '../datasets')
OUTPUT_PATH = os.path.join(os.getcwd(), '../output')

OUTPUT_REPORT_PATH = os.path.join(os.getcwd(), '../output/not_set/reports')
OUTPUT_CONVERGENCE_PATH = os.path.join(os.getcwd(), '../output/not_set/convergence')
OUTPUT_GRAPH_PATH = os.path.join(os.getcwd(), '../output/not_set/graphs')
OUTPUT_BEST_CONFIG_REPORT_PATH = os.path.join(os.getcwd(), '../output/not_set/best_config_report')
OUTPUT_JOINT_GRAPH_PATH = os.path.join(os.getcwd(), '../output/not_set/joint_graphs')
OUTPUT_COMPARISON_GRAPH_PATH = os.path.join(os.getcwd(), '../output/not_set/comparison_graphs')

PREFIX_COLOR_FFE = '92'
PREFIX_COLOR_ENCODER = '94'

max_ssim = 0
best_config_name = 'not_set'
time_out = False

MAX_VIOLATION = 1.5

RESOLUTIONS = [['VGA', '640', '480'], ['SVGA', '800', '600'], ['XGA', '1024', '768'], ['WXGA', '1280', '720'], ['KITTI', '1392', '512'], ['FHD', '1920', '1080'], ['QXGA', '2048', '1536']]

run_name = 'not_set'

dataset_length = 0
            

def get_dataset_lenght():
    return dataset_length


def set_system_timeout(dataset):
    global system_timeout
    global dataset_length
    dir = DATASETS_PATH + '/' + dataset
    onlyfiles = next(os.walk(dir))[2]

    # number of files in dir
    dataset_length = len(onlyfiles) # set dataset_length to number of frames
    system_timeout = dataset_length
    # multiply the frames with the timeout (total max duration for the frame compression)
    system_timeout *= (TIMEOUT)
    # add delay_start
    system_timeout += DELAY_START
    system_timeout = system_timeout/1000 # convert to seconds

    # round-up and convert to int  + *2 for some leeway
    system_timeout = int(ceil(system_timeout)) * 2 
    system_timeout += START_UP
    print('dataset length: ' + str(dataset_length))
    print('system timeout: ' + str(system_timeout)) 

def get_system_timeout():
    return system_timeout

# Returns folders in datasets directory
def get_datasets():
    datasets = os.listdir(DATASETS_PATH)
    valid_sets = []
    for dataset in datasets:
        files = next(os.walk(DATASETS_PATH + '/' + dataset))[2]
        is_set_valid = True
        for f in files:
            if not f[-4:] == '.png':
                is_set_valid = False
                print('A non-png file in: ' + str(dataset) + '. This might be an auto generated folder.')
        if is_set_valid:
            valid_sets.append(dataset)
    return valid_sets


# Returns the report_name in correct format
def generate_report_name(tag, resolution_name, config):
    report_name = get_dataset_name() + '-' + tag + '-' + resolution_name + '-' + 'C' + str(
        config) + '.csv'
    return report_name


# Iterates the generator and prints its log and sets time out
def log_helper(log_generator, color):
    for x in log_generator:
        print('\033[' + color + 'm### \033[0m' + (str(x, 'utf-8')))  # Prints with color code prefix and in utf-8
        if x == TIMED_OUT_MSG_BYTES:
            set_time_out()


# Saves list in output_name as name, creates dir output_path if not already exists
def save_list(list, name):
    if not os.path.isdir(OUTPUT_BEST_CONFIG_REPORT_PATH):
        os.mkdir(OUTPUT_BEST_CONFIG_REPORT_PATH)

    try:
        best_config_file = open(OUTPUT_BEST_CONFIG_REPORT_PATH + '/' + name, 'w')  # opens/creates file
        best_config_file.writelines(list)
        print("Best parameters saved: " + OUTPUT_BEST_CONFIG_REPORT_PATH + '/' + name)

    except Exception as e:
        try:
            print(
                'Saving best parameters in ' + OUTPUT_BEST_CONFIG_REPORT_PATH + ' failed. '
                'Saving best parameters in the same folder as the script. \n' +
                'Error: ' + str(e))

            best_config_file = open(os.getcwd() + '/' + name, 'w')  # opens/creates file
            best_config_file.writelines(list)
            print("Best parameters saved: " + os.getcwd() + '/' + name)

        except Exception:
            print("Failed to save best_config: " + name)


# Saves convergence graph
def save_convergence(axes, encoder, resolution_name):
    axes.set_ylim(top=1, bottom=0)
    axes.set_title(get_dataset_name() + '-' + encoder.TAG + '-' + resolution_name)

    figure = plt.gcf()
    figure.figsize = (16, 8)

    if not os.path.isdir(OUTPUT_CONVERGENCE_PATH):
        os.mkdir(OUTPUT_CONVERGENCE_PATH)

    try:
        plt.savefig(
            OUTPUT_CONVERGENCE_PATH + '/' + get_dataset_name() + '-'
            + encoder.TAG + '-' + resolution_name + '.png')

    except Exception as e:
        try:
            print(
                'Saving convergence graph in ' + OUTPUT_CONVERGENCE_PATH + ' failed. '
                'Saving graph in the same folder as the script. \n' +
                'Error: ' + str(e))
            plt.savefig(
                os.getcwd() + '/' + get_run_name() + '/' + get_dataset_name() + '-'
                + encoder.TAG + '-' + resolution_name + '.png')

        except Exception:
            print("Failed to save convergence graph: " + encoder.TAG + '-' + resolution_name)

    plt.clf()


# Returns coordinates so that the cropping will grow from the center/bottom line
def calculate_crop_x(initial_width, width):
    return str(int(initial_width) / 2 - (int(width) / 2))


def calculate_crop_y(initial_height, height):
    return str(int(initial_height) - (int(height)))


def set_time_out():
    global time_out
    time_out = True


def reset_time_out():
    global time_out
    time_out = False


def get_time_out():
    return time_out


def set_max_ssim(ssim):
    global max_ssim
    max_ssim = ssim


def get_max_ssim():
    return max_ssim


def set_best_config_name(name):
    global best_config_name
    best_config_name = name


def get_best_config_name():
    return best_config_name


def set_dataset(name):
    global pngs_path
    global dataset
    dataset = name
    pngs_path = os.path.join(os.getcwd(), '../datasets/' + name)


def get_pngs_path():
    return pngs_path


def get_output_report_path():
    return OUTPUT_REPORT_PATH


def get_best_config_report_path():
    return OUTPUT_BEST_CONFIG_REPORT_PATH


def get_output_graph_path():
    return OUTPUT_GRAPH_PATH


def get_joint_output_graph_path():
    return OUTPUT_JOINT_GRAPH_PATH

def get_comparison_output_graph_path():
    return OUTPUT_COMPARISON_GRAPH_PATH

def get_dataset_name():
    return dataset


# Checks if the config and the path are valid
def check_config_and_path(config_report_path, config_name, encoder_tag, resolution):
    if config_name == 'not_set':
        print(
            'No valid config for ' + get_dataset_name() + ' : ' + encoder_tag + ' : ' + resolution
            + ' found. Ignore res in graph')
        return False
    elif not config_report_path[-4:] == '.csv':
        print('Reports can only be of type .csv')
        return False
    else:
        return True


# Creates folders with the current date, time and machine
def set_run_name():
    dt = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    global run_name
    run_name = socket.gethostname() + '-' + dt

    if not os.path.isdir(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)

    path_current_run = OUTPUT_PATH + '/' + run_name
    if not os.path.isdir(path_current_run):
        os.mkdir(path_current_run)


# Updates the paths and creates folders used for the run and the specific dataset
def update_run_paths():
    path_current_run = OUTPUT_PATH + '/' + run_name + '/'+ get_dataset_name()
    if not os.path.isdir(path_current_run):
        os.mkdir(path_current_run)
        os.chmod(path_current_run, 0o777)   # # read/write by everyone

    global OUTPUT_REPORT_PATH
    global OUTPUT_CONVERGENCE_PATH
    global OUTPUT_GRAPH_PATH
    global OUTPUT_BEST_CONFIG_REPORT_PATH
    global OUTPUT_JOINT_GRAPH_PATH
    global OUTPUT_COMPARISON_GRAPH_PATH

    OUTPUT_REPORT_PATH = os.path.join(os.getcwd(), '../output/' + get_run_name() + '/' + get_dataset_name()
                                      + '/reports')
    OUTPUT_CONVERGENCE_PATH = os.path.join(os.getcwd(), '../output/' + get_run_name() + '/' + get_dataset_name()
                                           + '/convergence')
    OUTPUT_GRAPH_PATH = os.path.join(os.getcwd(), '../output/' + get_run_name() + '/' + get_dataset_name() + '/graphs')
    OUTPUT_BEST_CONFIG_REPORT_PATH = os.path.join(os.getcwd(), '../output/' + get_run_name() + '/' + get_dataset_name()
                                                  + '/best_config_report')
    OUTPUT_JOINT_GRAPH_PATH = os.path.join(os.getcwd(), '../output/' + get_run_name() + '/' + get_dataset_name() + '/joint_graphs')
    OUTPUT_COMPARISON_GRAPH_PATH = os.path.join(os.getcwd(), '../output/' + get_run_name() + '/' + get_dataset_name() + '/comparison_graphs')

def get_run_name():
    return run_name


class BestConfig:
    def __init__(self, best_config_report_path, best_config_name, resolution_name):
        self.best_config_report_path = best_config_report_path
        self.best_config_name = best_config_name
        self.resolution_name = resolution_name


class Encoder:
    def __init__(self, best_configs, encoder, dataset_name):
        self.best_configs = best_configs
        self.encoder = encoder
        self.dataset_name = dataset_name