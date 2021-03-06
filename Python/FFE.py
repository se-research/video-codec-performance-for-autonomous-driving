import utilities

_local_variables = {}

# Github repository, release version, and Docker tag
REPO = 'https://github.com/chrberger/frame-feed-evaluator.git'
VERSION = 'v0.0.4'
TAG = 'ffe:' + VERSION


def set_report_name(name):
    _local_variables['report_name'] = name


def initialize(init_width='0', init_height='0', width='0', height='0', report_name='not_set'):
    _local_variables['init_width'] = init_width
    _local_variables['init_height'] = init_height
    _local_variables['width'] = width
    _local_variables['height'] = height
    _local_variables['report_name'] = report_name


# Get the volumes for the Docker container
def get_volumes():
    return {'/tmp/': {'bind': '/tmp', 'mode': 'rw'},
            utilities.get_output_report_path(): {'bind': '/host', 'mode': 'rw'},
            utilities.get_pngs_path(): {
                'bind': '/pngs',
                'mode': 'rw'}
            }

# Get the commands used to when starting the Docker container
def get_commands():
    if _local_variables:
        if utilities.STOP_AFTER:
            return ['--folder=/pngs',
                    '--report=' + _local_variables['report_name'],
                    '--cid=' + utilities.CID,
                    '--name=' + utilities.SHARED_MEMORY_AREA,
                    '--crop.x=' + utilities.calculate_crop_x(_local_variables['init_width'], _local_variables['width']),
                    '--crop.y=' + utilities.calculate_crop_y(_local_variables['init_height'], _local_variables['height']),
                    '--crop.width=' + _local_variables['width'],
                    '--crop.height=' + _local_variables['height'],
                    '--delay=0',
                    '--delay.start=' + str(utilities.DELAY_START),
                    '--stopafter=' + str(utilities.STOP_AFTER_FRAMES),
                    '--timeout=' + str(utilities.TIMEOUT)
                    ]
        else:
            return ['--folder=/pngs',
                    '--report=' + _local_variables['report_name'],
                    '--cid=' + utilities.CID,
                    '--name=' + utilities.SHARED_MEMORY_AREA,
                    '--crop.x=' + utilities.calculate_crop_x(_local_variables['init_width'], _local_variables['width']),
                    '--crop.y=' + utilities.calculate_crop_y(_local_variables['init_height'], _local_variables['height']),
                    '--crop.width=' + _local_variables['width'],
                    '--crop.height=' + _local_variables['height'],
                    '--delay=0',
                    '--delay.start=' + str(utilities.DELAY_START),
                    '--timeout=' + str(utilities.TIMEOUT)
                    ]
    else:
        raise Exception('FFE was never initialized. Run the initialize method.')
