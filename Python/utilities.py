import os
import threading
import csv

CID = '112'
SHARED_MEMORY_AREA = 'video1'

STOP_AFTER = 80
TIMED_OUT_MSG_BYTES = str.encode('[frame-feed-evaluator]: Timed out while waiting for encoded frame.\n')
TIMED_OUT = 0

PNGS_PATH = os.path.join(os.getcwd(), '../2019-03-22_AstaZero_RuralRoad')
OUTPUT_REPORT_PATH = os.path.join(os.getcwd(), 'reports')

PREFIX_COLOR_FFE = '92'
PREFIX_COLOR_ENCODER = '94'

max_ssim = 0

def generate_report_name(tag, resolution_name, config):
        # update report name with this iteration's config
    # global config
    report_name = 'ffe-AstaZero_Rural_Road-' + tag + '-' + resolution_name + '-' + 'C' + str(
        config) + '.csv'
    return report_name
    
# Iterates the generator and prints its log and sets violation TIMED_OUT
def log_helper(log_generator, color):
    for x in log_generator:
        print('\033[' + color + 'm### \033[0m' + (str(x, 'utf-8')))  # Prints with color code prefix and in utf-8
        if x == TIMED_OUT_MSG_BYTES:
            global TIMED_OUT
            TIMED_OUT = 1


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


# Returns coordinates so that the cropping will grow from the center/bottom line
def calculate_crop_x(INITIAL_WIDTH, width):
    return str(int(INITIAL_WIDTH) / 2 - (int(width) / 2))


def calculate_crop_y(INITIAL_HEIGHT, height):
    return str(int(INITIAL_HEIGHT) - (int(height)))
