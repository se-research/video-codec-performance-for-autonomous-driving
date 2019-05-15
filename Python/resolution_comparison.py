import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
import csv
import os
import utilities
import plot_generator
import H264


def run(encoder_list):
    if len(encoder_list) < 1:
        print('No best_configs passed to resolution_comparison.')
    else:
        dataset = encoder_list[0].dataset_name
        resolutions = utilities.RESOLUTIONS
        ind = np.arange(len(resolutions))

        fig, ax = plt.subplots(figsize=(15, 15), sharey=True)
        par1 = ax.twinx()
        encs = {}
        x_positions = {}
        values = []
        keys = []
        count = 0
        for x in range(len(resolutions)):
            resolution = resolutions[x][0]
            best_configs = []
            encoders_and_configs = []
            for i, encoder in enumerate(encoder_list):

                # Returns indices for best_configs that has the current resolution
                indices = [idx for idx, bc in enumerate(encoder.best_configs) if bc.resolution_name == resolution]

                # if the list is not empty
                if indices:
                    path = encoder.best_configs[indices[0]].best_config_report_path
                    with open(path, 'r') as csvfile:
                        config_file = csv.reader(csvfile, delimiter=';')
                        tmp = []
                        for row in config_file:
                            tmp.append(float(row[10]))
                        encs[encoder.encoder] = mean(tmp)

            # Calculate other encode = rs as a percentage of H264 for each resolution.
            
            if H264.TAG in encs:
                for k, v in encs.items():
                    # Dont append the baseline value.
                    if k == H264.TAG:
                        continue
                    try:
                        per = ((v - encs[H264.TAG]) / encs[H264.TAG]) * 100
                        keys.append(k + '\n' + resolution)
                        values.append(per)
                        if resolution in x_positions:
                            x_positions[resolution] += 1
                        else:
                            x_positions[resolution] = 1
                    except ZeroDivisionError:
                        keys.append(k + '\n' + resolution)
                        values.append(0)
                        if resolution in x_positions:
                            x_positions[resolution] += 1
                        else:
                            x_positions[resolution] = 1

        # initialize our bar width and the subplot
        width = 0.2
        color_list = ['#aa0000', '#00aa00', '#0000aa', '#aa00aa', '#aaaa00', '#aaff00', '#44ff00']
        color_list = color_list[:len(encs.keys()) -1]
        rects1 = ax.bar(np.arange(1, len(keys) + 1), height = values, width = width, color=color_list)
        
        # Set our axes labels, title, tick marks, and then our x ticks.
        ax.set_ylabel('SSIM CHANGE')
        #ax.set_ylim(-20, 20)
        ax.set_title(dataset)
        ax.set_xticks(np.arange(1, len(keys) + 1))

        encs.pop(H264.TAG, None)
        ax.set_xticklabels(keys, rotation = 45, fontsize = 10)
        # Create a horizontal line at the origin
        ax.axhline(y=0, color='black')
        output_path = utilities.get_comparison_output_graph_path()
        plt.tick_params(axis='x', which='major', labelsize=10)
        
        labels = [item.get_text() for item in ax.get_yticklabels()]
        labels[0] = H264.TAG
        par1.set_yticklabels(labels)
        
        x_positions.popitem()
        for key in x_positions: 
            ax.axvline(x=count + x_positions[key] + 0.5, color='#000000')
            count += x_positions[key]
        plt.gcf().subplots_adjust(bottom=0.15)
        plt.tight_layout()

        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        try:
            plt.savefig(output_path + '/' + dataset + '.png')

        except Exception as e:
            try:
                print(
                    'Saving graph from resolution_comparison in ' + output_path + ' failed. '
                    'Saving graph in the same folder as the script. \n' +
                    'Error: ' + str(e))
                plt.savefig(
                    os.getcwd() + '/' + dataset + '.png')

            except Exception:
                print("Failed to graph from plot_generator: " + dataset)    
        
    plt.clf()