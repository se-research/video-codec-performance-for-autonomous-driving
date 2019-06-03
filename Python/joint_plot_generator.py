import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import utilities
import plot_generator


def run(encoder_list):
    if len(encoder_list) < 1:
        print('No best_configs passed to joint_plot_generator.')
    else:
        dataset = encoder_list[0].dataset_name
        resolutions = utilities.RESOLUTIONS

        for x in range(len(resolutions)):
            resolution = resolutions[x][0]
            best_configs = []
            encoders_and_configs = []

            for i, encoder in enumerate(encoder_list):

                # Returns indices for best_configs that has the current resolution
                index = [idx for idx, bc in enumerate(encoder.best_configs) if bc.resolution_name == resolution]

                if index:
                    best_config = encoder.best_configs[index[0]]  # Use first index item

                    best_configs.append(best_config)

                    # Extract config number from best config name.
                    firstStep = best_config.best_config_name.split('.')[-2]
                    secondStep = firstStep.split('-')[-1]
                    encoders_and_configs.append(encoder.encoder + '\n' + secondStep)

                    y_ssim = []

                    fig, ax = plt.subplots(figsize=(16, 8))

                    ax.autoscale_view(scalex=True)

                    ax.tick_params(axis='y', colors='#ee0000')

                    ax.set_title(dataset + ' : [' + resolution + ']', fontsize='xx-large')

                    ax.set_ylabel('ssim', color='#ee0000', fontsize='x-large')

                    for i, bc in enumerate(best_configs):
                        with open(bc.best_config_report_path, 'r') as csvfile:
                            plots = csv.reader(csvfile, delimiter=';')
                            tmp = []
                            for row in plots:
                                tmp.append(float(row[10]))
                            y_ssim.append(tmp)

                    ssim_boxes = ax.boxplot(y_ssim, showfliers=False, patch_artist=True)

                    # Fill with colors.
                    plot_generator.colorize_boxes(ssim_boxes, '#cc0000', '#aa0000')

                    plt.xticks(np.arange(1, len(best_configs) + 1, step=1), encoders_and_configs)

                    output_path = utilities.get_joint_output_graph_path()

                    if not os.path.isdir(output_path):
                        os.mkdir(output_path)

                    try:
                        plt.savefig(output_path + '/' + dataset + '-' + resolution + '.png')

                    except Exception as e:
                        try:
                            print(
                                'Saving graph from plot_generator in ' + output_path + ' failed. '
                                'Saving graph in the same folder as the script. \n' +
                                'Error: ' + str(e))
                            plt.savefig(
                                os.getcwd() + '/' + dataset + '-' + resolution + '.png')

                        except Exception:
                            print("Failed to graph from plot_generator: " + dataset + '-' + resolution)

        plt.clf()
