import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import csv
import sys

# Find files.
files = []
for x in sys.argv[1:]:
    if not len(sys.argv[1:]) == 6:
        print('Not enough input files entered as parameters. Must be 6 '
        + '(One for each resoution). \n '
        + 'Example filename parameter: ffe-x264-vga-ultrafast.csv')
        sys.exit()

    if not x[-4:] == '.csv':
        print('Params can only be of type .csv')
        sys.exit()
    files.append(x)

y_ssim = []
y_size = []
y_time = []

def make_axis_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

# Multiple box plots on one Axes
fig, ax = plt.subplots(sharey=False, sharex=True)
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

scenario = ''
codec = ''
resolutions = []
configs = []
for file in files:
    #Adding the different resoulutions
    # and configs to resolution_list & config_list
    tmp = file.split('-')
    scenario = tmp[1].replace('_', ' ')
    codec = tmp[2]
    resolutions.append(tmp[3])
    substring = tmp[4]
    substring = substring[:-4]
    configs.append(substring)

# Todo: Choose correct scenario name.
ax.set_title(scenario + ': ' + codec)

ax.set_ylabel('ssim')
par1.set_ylabel('size')
par2.set_ylabel('time')

position_x = [[], [], []]
ssim_x = 1
size_x = 2
time_x = 3

for i, file in enumerate(files):
    with open(file, 'r') as csvfile:
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
        ssim_x += 3
        size_x += 3
        time_x += 3
        tmp_ssim = []
        tmp_size = []
        tmp_time = []

ssim_boxes = ax.boxplot(y_ssim, positions=position_x[0], showfliers=False, whis=[0, 100], patch_artist=True)
size_boxes = par1.boxplot(y_size, positions=position_x[1], showfliers=False, whis=[0, 100], patch_artist=True)
time_boxes = par2.boxplot(y_time, positions=position_x[2], showfliers=False, whis=[0, 100], patch_artist=True)

def colorize_boxes(boxes, color, linecolor):
    for box in boxes['boxes']:
        # change outline color
        box.set(color = color, linewidth=1)
        # change fill color
        box.set(facecolor = linecolor)

def get_metrics(arr_of_arrays):
    d = dict()
    mins = []
    maxes = []
    for arr in arr_of_arrays:
        # Fill on quartiles
        mins.append(np.percentile(arr, 75))
        maxes.append(np.percentile(arr, 25))
        # Fill on whiskers.
        #mins.append(min(arr))
        #maxes.append(max(arr))
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

# Fill with colors.
colorize_boxes(ssim_boxes, '#aa0000', '#cc0000')
colorize_boxes(size_boxes, '#00aa00', '#00cc00')
colorize_boxes(time_boxes, '#0000aa', '#0000cc')

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
for r in resolutions:
    for c in configs:
        resolution_and_configs.append(r.upper() + '\n' + c)

plt.xticks(np.arange(2, x_width, step=3), resolution_and_configs)
# plt.show()
plt.savefig(scenario + '-' + codec + '.png')
