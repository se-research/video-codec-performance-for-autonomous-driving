import utilities

_local_variables = {}

REPO = 'https://github.com/chrberger/frame-feed-evaluator.git'
VERSION = 'v0.0.4'
TAG = 'ffe:' + VERSION

VOLUMES = {'/tmp/': {'bind': '/tmp', 'mode': 'rw'},
           utilities.OUTPUT_REPORT_PATH: {'bind': '/host', 'mode': 'rw'},
           utilities.PNGS_PATH: {
               'bind': '/pngs',
               'mode': 'rw'}
           }


def initialize(init_width='0', init_height='0', width='0', height='0', report_name='not_set'):
    _local_variables['init_width'] = init_width
    _local_variables['init_height'] = init_height
    _local_variables['width'] = width
    _local_variables['height'] = height
    _local_variables['report_name'] = report_name


def get_commands():
    if _local_variables:
        return ['--folder=/pngs',
                '--report=' + _local_variables['report_name'],
                '--cid=' + utilities.CID,
                '--name=' + utilities.SHARED_MEMORY_AREA,
                '--crop.x=' + utilities.calculate_crop_x(_local_variables['init_width'], _local_variables['width']),
                '--crop.y=' + utilities.calculate_crop_y(_local_variables['init_height'], _local_variables['height']),
                '--crop.width=' + _local_variables['width'],
                '--crop.height=' + _local_variables['height'],
                '--delay=0',
                '--delay.start=200',
                '--stopafter=' + str(utilities.STOP_AFTER),
                # '--noexitontimeout'
                # '--verbose',
                ]
    else:
        raise Exception('FFE was never initialized. Run the initialize method.')
