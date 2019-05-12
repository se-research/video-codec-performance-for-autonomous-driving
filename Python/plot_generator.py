import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import utilities


# Find files.
def run(best_configs, dataset, codec):
    if len(best_configs) < 1:
        print('No best_configs passed to plot_generator.')
    else:
        y_ssim = []
        y_size = []
        y_time = []

        def make_axis_invisible(ax):
            ax.set_frame_on(True)
            ax.patch.set_visible(False)
            for sp in ax.spines.values():
                sp.set_visible(False)

        # Multiple box plots on one Axes
        fig, ax = plt.subplots(sharey=False, sharex=True, figsize=(16, 8))
        fig.subplots_adjust(right=0.75)

        ax.autoscale_view(scalex=True)
        # Add parallell axes
        par1 = ax.twinx()
        par2 = ax.twinx()

        par2.spines["right"].set_position(("axes", 1.2))
        make_axis_invisible(par2)
        par2.spines["right"].set_visible(True)

        ax.tick_params(axis='y', colors='#ee0000')
        par1.tick_params(axis='y', colors='#00ee00')
        par2.tick_params(axis='y', colors='#0000ee')

        ax.set_ylim(top=1, bottom=0)
        par1.set_ylim(top=65600, bottom=0)
        par2.set_ylim(top=40000, bottom=0)

        ax.set_title(dataset + ' : [' + codec + ']')

        ax.set_ylabel('ssim', color='#ee0000', fontsize='x-large')
        par1.set_ylabel('size', color='#00ee00', fontsize='x-large')
        par2.set_ylabel('time', color='#0000ee', fontsize='x-large')

        position_x = [[], [], []]
        ssim_x = 1
        size_x = 2
        time_x = 3

        for i, bc in enumerate(best_configs):
            with open(bc.best_config_report_path, 'r') as csvfile:
                plots = csv.reader(csvfile, delimiter=';')
                tmp_ssim = []
                tmp_size = []
                tmp_time = []
                for row in plots:
                    tmp_ssim.append(float(row[10]))
                    tmp_size.append(float(row[6]))
                    tmp_time.append(float(row[12]))
                y_ssim.append(tmp_ssim)
                y_size.append(tmp_size)
                y_time.append(tmp_time)

                position_x[1].append(size_x)
                position_x[0].append(ssim_x)
                position_x[2].append(time_x)
                # Do not add delimiter line on the last item.
                if not i == (len(best_configs) - 1):
                    ax.axvline(x=time_x + 0.5, color='#000000')
                ssim_x += 3
                size_x += 3
                time_x += 3
                tmp_ssim = []
                tmp_size = []
                tmp_time = []

        ssim_boxes = ax.boxplot(y_ssim, positions=position_x[0], showfliers=False, patch_artist=True)
        size_boxes = par1.boxplot(y_size, positions=position_x[1], showfliers=False, patch_artist=True)
        time_boxes = par2.boxplot(y_time, positions=position_x[2], showfliers=False, patch_artist=True)

        # Fill with colors.
        colorize_boxes(ssim_boxes, '#cc0000', '#aa0000')
        colorize_boxes(size_boxes, '#00cc00', '#00aa00')
        colorize_boxes(time_boxes, '#0000cc', '#0000aa')

        # Get median, min and max.
        ssim_metric_dict = get_metrics(y_ssim)
        ssim_median_line = get_median(ssim_boxes)

        size_metric_dict = get_metrics(y_size)
        size_median_line = get_median(size_boxes)

        time_metric_dict = get_metrics(y_time)
        time_median_line = get_median(time_boxes)
        # Plotting min and max.
        plot_min_max_with_fill(position_x[0], ax, ssim_metric_dict, ssim_median_line, '#ff0000')
        plot_min_max_with_fill(position_x[1], par1, size_metric_dict, size_median_line, '#00ff00')
        plot_min_max_with_fill(position_x[2], par2, time_metric_dict, time_median_line, '#0000ff')

        x_width = position_x[2][-1] + 1
        plt.xlim([0, x_width])

        resolution_and_configs = []
        for bc in best_configs:
            resolution_and_configs.append(bc.resolution_name + '\n')

        # Extract config number from best config name.
        for i, bc in enumerate(best_configs):
            firstStep = bc.best_config_name.split('.')[-2]
            secondStep = firstStep.split('-')[-1]
            resolution_and_configs[i] += secondStep

        plt.xticks(np.arange(2, x_width, step=3), resolution_and_configs)

        output_path = utilities.get_output_graph_path()

        if not os.path.isdir(output_path):
            os.mkdir(output_path)

        try:
            plt.savefig(output_path + '/' + dataset + '-' + codec + '.png')

        except Exception as e:
            try:
                print(
                    'Saving graph from plot_generator in ' + output_path + ' failed. '
                    'Saving graph in the same folder as the script. \n' +
                    'Error: ' + str(e))
                plt.savefig(
                    os.getcwd() + '/' + dataset + '-' + codec + '.png')

            except Exception:
                print("Failed to graph from plot_generator: " + dataset + '-' + codec)

    plt.clf()


def colorize_boxes(boxes, color, linecolor):
    for box in boxes['boxes']:
        # Change outline color
        box.set(color=color, linewidth=1, alpha=0.7)
        # Change fill color
        box.set(facecolor=linecolor)


def get_metrics(arr_of_arrays):
    d = dict()
    mins = []
    maxes = []
    for arr in arr_of_arrays:
        # Fill on quartiles
        mins.append(np.percentile(arr, 75))
        maxes.append(np.percentile(arr, 25))
        # Fill on whiskers.
        # mins.append(min(arr))
        # maxes.append(max(arr))
    d['min'] = mins
    d['max'] = maxes
    return d


def get_median(boxes):
    median_line = []
    for medline in boxes['medians']:
        linedata = medline.get_ydata()
        median = linedata[0]
        median_line.append(median)
    return median_line


def plot_min_max_with_fill(x_positions, ax, metric_dict, median_line, color):
    min_plot = ax.plot(x_positions, metric_dict['min'], color=color, lw=1, alpha=0.2)
    max_plot = ax.plot(x_positions, metric_dict['max'], color=color, lw=1, alpha=0.2)
    median_plot = ax.plot(x_positions, median_line, color='#f4a742', lw=1, alpha=0.2)
    ax.fill_between(x_positions, metric_dict['min'], metric_dict['max'], color=color, alpha=0.1)

    d = dict()
    d['min_plot'] = min_plot
    d['max_plot'] = max_plot
    d['median_plot'] = median_plot

    return d
