REPO_VPX_FULL = 'https://github.com/jeberlen/opendlv-video-vpx-encoder.git'
VERSION_ENCODER = 'latest'
TAG_ENCODER = 'vpx-full:' + VERSION_ENCODER
PREFIX_COLOR_ENCODER = '94'

"""
def get_list_encoder_vp9_full():
    return ['--cid=' + CID,
            '--name=' + SHARED_MEMORY_AREA,
            '--width=' + width,
            '--height=' + height,
            # '--verbose',
            ###################
            '--gop=' + str(gop),
            '--threads=' + str(g_threads),
            '--profile=' + str(g_profile),
            '--lag-in-frame=' + str(g_lag_in_frames),
            '--drop-frame=' + str(rc_dropframe_thresh),
            '--resize-allowed=' + str(rc_resize_allowed),
            '--resize-up=' + str(rc_resize_up_thresh),
            '--resize-down=' + str(rc_resize_down_thresh),
            '--undershoot-pct=' + str(rc_undershoot_pct),
            '--overshoot-pct=' + str(rc_overshoot_pct),
            '--min-q=' + str(rc_min_quantizer),
            '--max-q=' + str(rc_max_quantizer),
            '--end-usage=' + str(rc_end_usage),
            '--buffer-size=' + str(rc_buf_sz),
            '--buffer-init-size=' + str(rc_buf_initial_sz),
            '--buffer-optimal-size=' + str(rc_buf_optimal_sz),
            '--bitrate=' + str(rc_target_bitrate),
            '--kf-mode=' + str(kf_mode),
            '--kf-min-dist=' + str(kf_min_dist),
            '--kf-max-dist=' + str(kf_max_dist)
            ]
"""

#####################
# http://doxygen.db48x.net/mozilla/html/structvpx__codec__enc__cfg.html
# Parameters according to https://www.webmproject.org/docs/encoder-parameters/

# gop = 1 # 1 - n of frames

g_timebase_num = 1  # Unsure if we need to change
g_timebase_den = 20  # Unsure if we need to change
g_threads = 1  # 1 - 4
g_profile = 0  # 0 - 1
g_lag_in_frames = 0  # 0 - 25 (over 12 turns on alt-ref frame, a VPx quality enhancer)

rc_dropframe_thresh = 0.0  # 0.0 - 1.0
rc_resize_allowed = 0  # 0 - 1
rc_resize_up_thresh = 0.0  # 0.0 - 1.0
rc_resize_down_thresh = 0.0  # 0.0 - 1.0
rc_undershoot_pct = 0  # 0 - 100 | VP8 ? 0 - 1000
rc_overshoot_pct = 0  # 0 - 100 | VP8 ? 0 - 1000
rc_min_quantizer = 0  # 0 - 52 | VP8 ? 0 - 56
rc_max_quantizer = 0  # 0 - 52 | VP8 ? 0 - 56
rc_end_usage = 0  # 0 - 1
rc_buf_sz = 0  # 0 - 60000
rc_buf_initial_sz = 0  # 0 - 40000
rc_buf_optimal_sz = 0  # 0 - 50000
rc_target_bitrate = 100000  # 100000 - 5000000

kf_mode = 0  # 0 - 1
kf_min_dist = 0  # 0 - n of frames
kf_max_dist = 0  # 0 - n of frames