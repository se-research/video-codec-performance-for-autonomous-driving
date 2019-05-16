import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
import csv
import os
import utilities
import plot_generator
import H264
import VP9
import QSV_H264
import QSV_VP9


def run(encoder_list):
    if len(encoder_list) < 1:
        print('No best_configs passed to resolution_comparison.')
    else:
        dataset = encoder_list[0].dataset_name
        resolutions = utilities.RESOLUTIONS

        fig, ax = plt.subplots(figsize=(15, 15), sharey=True)
        par_x = ax.twiny()

        encs = {}
        x_positions = {}
        values = []
        keys = []
        colors = []
        clean_resolutions = {}
        for x in range(len(resolutions)):
            resolution = resolutions[x][0]
            width = resolutions[x][1]
            height = resolutions[x][2]
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
                        clean_resolutions[resolution + ' (' + width + 'x' +height + ')'] = 0
                        keys.append(k)
                        values.append(per)
                        if(k == VP9.TAG):
                            colors.append('#cc0000')

                        elif(k == QSV_H264.TAG):
                            colors.append('#0000cc')
                        elif(k == QSV_VP9.TAG):
                            colors.append('#00cc00')
                        else:
                            colors.append('#aaaa00')

                        if resolution in x_positions:
                            x_positions[resolution] += 1
                        else:
                            x_positions[resolution] = 1
                    except ZeroDivisionError:
                        keys.append(k)
                        values.append(0)
                        if resolution in x_positions:
                            x_positions[resolution] += 1
                        else:
                            x_positions[resolution] = 1
            encs = {}

        # initialize our bar width and the subplot
        width = 0.2
        rects1 = ax.bar(np.arange(1, len(keys) + 1), height = values, width = width, color=colors)
        
        # Set our axes labels, title, tick marks, and then our x ticks.
        ax.set_ylabel('SSIM change in percentage', fontsize='x-large')
        #ax.set_ylim(-20, 20)
        ax.set_title(dataset, fontsize='xx-large')
        ax.set_xticks(np.arange(1, len(keys) + 1))
        
        encs.pop(H264.TAG, None)
    
        ax.set_xticklabels(keys, rotation = 45, fontsize = 10)
        # Create a horizontal line at the origin
        ax.axhline(y=0, color='black', label=H264.TAG, linestyle='--')
        output_path = utilities.get_comparison_output_graph_path()
        plt.tick_params(axis='x', which='major', labelsize=10)
        
        x2_steps = []
        step_count = 0
        for key in x_positions:  
            x2_steps.append(step_count + ((x_positions[key] + 1) / 2))
            step_count += x_positions[key]
      
        if x_positions:
            x_positions.popitem()

        count = 0
        for key in x_positions: 
            ax.axvline(x=count + x_positions[key] + 0.5, color='#000000')
            count += x_positions[key]
        

        par_x.set_xlim(ax.get_xlim())
        par_x.set_xticks(x2_steps)
        if clean_resolutions.keys():
            par_x.set_xticklabels(clean_resolutions.keys())

        ax.legend()
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