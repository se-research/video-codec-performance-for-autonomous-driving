import os
import matplotlib.pyplot as plt

CID = '112'
SHARED_MEMORY_AREA = 'video1'

STOP_AFTER = 80
TIMED_OUT_MSG_BYTES = str.encode('[frame-feed-evaluator]: Timed out while waiting for encoded frame.\n')
TIMED_OUT = False

PNGS_PATH = os.path.join(os.getcwd(), '../2019-03-22_AstaZero_RuralRoad')
OUTPUT_REPORT_PATH = os.path.join(os.getcwd(), 'reports')
OUTPUT_CONVERGENCE_PATH = os.path.join(os.getcwd(), 'convergence')
OUTPUT_GRAPH_PATH = os.path.join(os.getcwd(), 'graphs')
OUTPUT_BEST_CONFIG_REPORT_PATH = os.path.join(os.getcwd(), 'best_configs_report')

PREFIX_COLOR_FFE = '92'
PREFIX_COLOR_ENCODER = '94'

max_ssim = 0
best_config_name = 'not_set'
time_out = False


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

    # returns the report_name in correct format
def generate_report_name(tag, resolution_name, config):
    report_name = 'ffe-AstaZero_Rural_Road-' + tag + '-' + resolution_name + '-' + 'C' + str(
        config) + '.csv'
    return report_name


# Iterates the generator and prints its log and sets time out
def log_helper(log_generator, color):
    for x in log_generator:
        print('\033[' + color + 'm### \033[0m' + (str(x, 'utf-8')))  # Prints with color code prefix and in utf-8
        if x == TIMED_OUT_MSG_BYTES:
            set_time_out()


# Saves list in output_name as name, creates dir output_path if not already exists
def save_list(list, output_path, name):
    if os.path.isdir(output_path):
        best_config_file = open(output_path + '/' + name, 'w')  # opens/creates file
        best_config_file.writelines(list)
        print("Best parameters saved: " + output_path + '/' + name)
    else:
        try:
            os.mkdir(output_path)
            best_config_file = open(output_path + '/' + name, 'w')  # opens/creates file
            best_config_file.writelines(list)
            print("Best parameters saved: " + output_path + '/' + name)
        except Exception as e:
            print("Creation of the dir %s failed. " + e % output_path)


# Saves convergence graph
def save_convergence(axes, encoder, resolution_name):
    axes.set_ylim(top=1, bottom=0)
    axes.set_title('AstaZero_Rural_Road-' + encoder.TAG + '-' + resolution_name)

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


# Returns coordinates so that the cropping will grow from the center/bottom line
def calculate_crop_x(initial_width, width):
    return str(int(initial_width) / 2 - (int(width) / 2))


def calculate_crop_y(initial_height, height):
    return str(int(initial_height) - (int(height)))
