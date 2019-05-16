import VP9
import H264
import QSV_VP9
import QSV_H264


# Returns default config for the specific dataset, encoder and resolution. If aforementioned combination
# is absent in DefaultConfigs, None is return and no default config is used to initialize the optimization
class DefaultConfigs:
    def __init__(self, encoder, dataset, resolution):
        self.config = None

        if dataset == 'KITTI_DRIVE_0071':
            self.config = KITTI_DRIVE_0071(resolution, encoder).config
        elif dataset == '2019-03-22-AstaZero-RuralRoad':
            self.config = AstaZero_RuralRoad(resolution, encoder).config
        elif dataset == '2019-04-17-COPPLAR':
            self.config = COPPLAR(resolution, encoder).config
        else:
            print('No default config found for the dataset, encoder and resolution')
            self.config = None


class KITTI_DRIVE_0071:
    def __init__(self, resolution, encoder):
        self.config = None

        if resolution == 'KITTI':
            if encoder == VP9.TAG:
                self.config = [250,  # gop
                               0,  # drop_frame
                               0,  # resize_allowed
                               100,  # resize_up
                               100,  # resize_down
                               100,  # undershoot_pct
                               0,  # overshoot_pct
                               41,  # min_q
                               1,  # end_usage
                               6000,  # buffer_size
                               444,  # buffer_init_size
                               3547,  # buffer_optimal_size
                               5000000,  # bitrate
                               0,  # kf_mode
                               0,  # kf_min_dist
                               250,  # kf_max_dist
                               6  # cpu_used
                               ]

            elif encoder == H264.TAG:
                self.config = [5000000,  # bitrate
                               194700,  # max_bitrate
                               250,  # qop
                               0,  # rc_mode
                               2,  # ecomplexity
                               2,  # sps_pps_strategy
                               1,  # num_ref_frame
                               1,  # ssei
                               1,  # prefix_nal
                               0,  # entropy_coding
                               1,  # frame_skip
                               0,  # qp_max
                               50,  # qp_min
                               1,  # long_term_ref
                               0,  # loop_filter
                               1,  # denoise
                               0,  # background_detection
                               1,  # adaptive_quant
                               0,  # frame_cropping
                               1,  # scene_change_detect
                               0,  # padding
                               ]

            elif encoder == QSV_VP9.TAG:
                self.config = [10,  # gop
                               2000,  # bitrate
                               0,  # ip-period
                               26,  # init-qp
                               1,  # qpmin
                               51,  # qpmax
                               0,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               1,  # num-ref-frame
                               4,  # rc-mode
                               0,  # reference-mode
                               ]

            elif encoder == QSV_H264.TAG:
                self.config = [47,  # gop
                               2474,  # bitrate
                               35,  # ip-period
                               37,  # init-qp
                               24,  # qpmin
                               25,  # qpmax
                               0,  # disable-frame-skip
                               7,  # diff-qp-ip
                               21,  # diff-qp-ib
                               9,  # num-ref-frame
                               2,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               0,  # deblock-filter
                               1,  # prefix-nal
                               45,  # idr-interval
                               ]


class AstaZero_RuralRoad:
    def __init__(self, resolution, encoder):
        self.config = None

        ##################################################### VP9 ######################################################
        if encoder == VP9.TAG:
            if resolution == 'VGA':
                self.config = [26,  # gop
                               67,  # drop_frame
                               0,  # resize_allowed
                               87,  # resize_up
                               30,  # resize_down
                               22,  # undershoot_pct
                               85,  # overshoot_pct
                               17,  # min_q
                               1,  # end_usage
                               3264,  # buffer_size
                               3268,  # buffer_init_size
                               3519,  # buffer_optimal_size
                               2168373,  # bitrate
                               1,  # kf_mode
                               0,  # kf_min_dist
                               93,  # kf_max_dist
                               8  # cpu_used
                               ]

            elif resolution == 'SVGA':
                self.config = [159,  # gop
                               0,  # drop_frame
                               1,  # resize_allowed
                               0,  # resize_up
                               93,  # resize_down
                               95,  # undershoot_pct
                               16,  # overshoot_pct
                               13,  # min_q
                               0,  # end_usage
                               6000,  # buffer_size
                               1147,  # buffer_init_size
                               0,  # buffer_optimal_size
                               3895523,  # bitrate
                               1,  # kf_mode
                               1,  # kf_min_dist
                               163,  # kf_max_dist
                               9  # cpu_used
                               ]
            elif resolution == 'XGA':
                self.config = [68,  # gop
                               18,  # drop_frame
                               1,  # resize_allowed
                               90,  # resize_up
                               100,  # resize_down
                               31,  # undershoot_pct
                               31,  # overshoot_pct
                               44,  # min_q
                               1,  # end_usage
                               5425,  # buffer_size
                               4000,  # buffer_init_size
                               1445,  # buffer_optimal_size
                               2194015,  # bitrate
                               0,  # kf_mode
                               0,  # kf_min_dist
                               173,  # kf_max_dist
                               6  # cpu_used
                               ]
            elif resolution == 'WXGA':
                self.config = [243,  # gop
                               0,  # drop_frame
                               1,  # resize_allowed
                               73,  # resize_up
                               28,  # resize_down
                               20,  # undershoot_pct
                               0,  # overshoot_pct
                               26,  # min_q
                               0,  # end_usage
                               0,  # buffer_size
                               0,  # buffer_init_size
                               3275,  # buffer_optimal_size
                               3559766,  # bitrate
                               1,  # kf_mode
                               0,  # kf_min_dist
                               0,  # kf_max_dist
                               8  # cpu_used
                               ]
            elif resolution == 'KITTI':
                self.config = [250,  # gop
                               0,  # drop_frame
                               0,  # resize_allowed
                               100,  # resize_up
                               100,  # resize_down
                               100,  # undershoot_pct
                               0,  # overshoot_pct
                               41,  # min_q
                               1,  # end_usage
                               6000,  # buffer_size
                               444,  # buffer_init_size
                               3547,  # buffer_optimal_size
                               5000000,  # bitrate
                               0,  # kf_mode
                               0,  # kf_min_dist
                               250,  # kf_max_dist
                               6  # cpu_used
                               ]
            elif resolution == 'FHD':
                self.config = [250,  # gop
                               0,  # drop_frame
                               0,  # resize_allowed
                               100,  # resize_up
                               100,  # resize_down
                               100,  # undershoot_pct
                               0,  # overshoot_pct
                               41,  # min_q
                               1,  # end_usage
                               6000,  # buffer_size
                               444,  # buffer_init_size
                               3547,  # buffer_optimal_size
                               5000000,  # bitrate
                               0,  # kf_mode
                               0,  # kf_min_dist
                               250,  # kf_max_dist
                               16  # cpu_used
                               ]
            elif resolution == 'QXGA':
                self.config = [250,  # gop
                               0,  # drop_frame
                               0,  # resize_allowed
                               100,  # resize_up
                               100,  # resize_down
                               100,  # undershoot_pct
                               0,  # overshoot_pct
                               41,  # min_q
                               1,  # end_usage
                               6000,  # buffer_size
                               444,  # buffer_init_size
                               3547,  # buffer_optimal_size
                               5000000,  # bitrate
                               0,  # kf_mode
                               0,  # kf_min_dist
                               250,  # kf_max_dist
                               16  # cpu_used
                               ]

        ##################################################### H264 #####################################################
        if encoder == H264.TAG:
            if resolution == 'VGA':
                self.config = [446583,  # bitrate
                               100000,  # max_bitrate
                               250,  # qop
                               0,  # rc_mode
                               0,  # ecomplexity
                               0,  # sps_pps_strategy
                               16,  # num_ref_frame
                               1,  # ssei
                               0,  # prefix_nal
                               1,  # entropy_coding
                               1,  # frame_skip
                               0,  # qp_max
                               50,  # qp_min
                               0,  # long_term_ref
                               2,  # loop_filter
                               0,  # denoise
                               0,  # background_detection
                               1,  # adaptive_quant
                               1,  # frame_cropping
                               0,  # scene_change_detect
                               1]  # padding

            elif resolution == 'SVGA':
                self.config = [4753765,  # bitrate
                               1938988,  # max_bitrate
                               144,  # qop
                               0,  # rc_mode
                               0,  # ecomplexity
                               0,  # sps_pps_strategy
                               1,  # num_ref_frame
                               0,  # ssei
                               1,  # prefix_nal
                               0,  # entropy_coding
                               1,  # frame_skip
                               41,  # qp_max
                               0,  # qp_min
                               1,  # long_term_ref
                               0,  # loop_filter
                               0,  # denoise
                               1,  # background_detection
                               1,  # adaptive_quant
                               1,  # frame_cropping
                               0,  # scene_change_detect
                               1  # padding
                               ]
            elif resolution == 'XGA':
                self.config = [5000000,  # bitrate
                               100000,  # max_bitrate
                               250,  # qop
                               0,  # rc_mode
                               0,  # ecomplexity
                               3,  # sps_pps_strategy
                               1,  # num_ref_frame
                               0,  # ssei
                               1,  # prefix_nal
                               1,  # entropy_coding
                               0,  # frame_skip
                               0,  # qp_max
                               50,  # qp_min
                               1,  # long_term_ref
                               2,  # loop_filter
                               1,  # denoise
                               0,  # background_detection
                               0,  # adaptive_quant
                               1,  # frame_cropping
                               0,  # scene_change_detect
                               0  # padding
                               ]
            elif resolution == 'WXGA':
                self.config = [100000,  # bitrate
                               100000,  # max_bitrate
                               250,  # qop
                               0,  # rc_mode
                               0,  # ecomplexity
                               1,  # sps_pps_strategy
                               1,  # num_ref_frame
                               0,  # ssei
                               1,  # prefix_nal
                               0,  # entropy_coding
                               1,  # frame_skip
                               0,  # qp_max
                               0,  # qp_min
                               0,  # long_term_ref
                               2,  # loop_filter
                               0,  # denoise
                               0,  # background_detection
                               1,  # adaptive_quant
                               0,  # frame_cropping
                               0,  # scene_change_detect
                               0,  # padding
                               ]
            elif resolution == 'KITTI':
                self.config = [5000000,  # bitrate
                               194700,  # max_bitrate
                               250,  # qop
                               0,  # rc_mode
                               2,  # ecomplexity
                               2,  # sps_pps_strategy
                               1,  # num_ref_frame
                               1,  # ssei
                               1,  # prefix_nal
                               0,  # entropy_coding
                               1,  # frame_skip
                               0,  # qp_max
                               50,  # qp_min
                               1,  # long_term_ref
                               0,  # loop_filter
                               1,  # denoise
                               0,  # background_detection
                               1,  # adaptive_quant
                               0,  # frame_cropping
                               1,  # scene_change_detect
                               0  # padding
                               ]
            elif resolution == 'FHD':
                self.config = [1500000,  # bitrate
                               5000000,  # max_bitrate
                               10,  # qop
                               0,  # rc_mode
                               0,  # ecomplexity
                               0,  # sps_pps_strategy
                               1,  # num_ref_frame
                               0,  # ssei
                               0,  # prefix_nal
                               0,  # entropy_coding
                               1,  # frame_skip
                               42,  # qp_max
                               12,  # qp_min
                               0,  # long_term_ref
                               0,  # loop_filter
                               0,  # denoise
                               1,  # background_detection
                               1,  # adaptive_quant
                               1,  # frame_cropping
                               1,  # scene_change_detect
                               1  # padding
                               ]
            elif resolution == 'QXGA':
                self.config = [1778179,  # bitrate
                               2551222,  # max_bitrate
                               230,  # qop
                               2,  # rc_mode
                               0,  # ecomplexity
                               1,  # sps_pps_strategy
                               3,  # num_ref_frame
                               1,  # ssei
                               0,  # prefix_nal
                               1,  # entropy_coding
                               1,  # frame_skip
                               39,  # qp_max
                               40,  # qp_min
                               0,  # long_term_ref
                               0,  # loop_filter
                               1,  # denoise
                               0,  # background_detection
                               1,  # adaptive_quant
                               0,  # frame_cropping
                               0,  # scene_change_detect
                               1  # padding
                               ]

        ################################################### QSV-H264 ###################################################
        if encoder == QSV_H264.TAG:
            if resolution == 'VGA':
                self.config = [160,  # gop
                               2868,  # bitrate
                               20,  # ip-period
                               25,  # init-qp
                               1,  # qpmin
                               25,  # qpmax
                               0,  # disable-frame-skip
                               12,  # diff-qp-ip
                               31,  # diff-qp-ib
                               10,  # num-ref-frame
                               1,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               1,  # dct8x8
                               0,  # deblock-filter
                               0,  # prefix-nal
                               31,  # idr-interval
                               ]
            elif resolution == 'SVGA':
                self.config = [225,  # gop
                               2253,  # bitrate
                               35,  # ip-period
                               13,  # init-qp
                               27,  # qpmin
                               41,  # qpmax
                               1,  # disable-frame-skip
                               20,  # diff-qp-ip
                               17,  # diff-qp-ib
                               11,  # num-ref-frame
                               3,  # rc-mode
                               1,  # profile
                               1,  # cabac
                               1,  # dct8x8
                               0,  # deblock-filter
                               0,  # prefix-nal
                               22,  # idr-interval
                               ]
            elif resolution == 'XGA':
                self.config = [47,  # gop
                               2474,  # bitrate
                               35,  # ip-period
                               37,  # init-qp
                               24,  # qpmin
                               25,  # qpmax
                               0,  # disable-frame-skip
                               7,  # diff-qp-ip
                               21,  # diff-qp-ib
                               9,  # num-ref-frame
                               2,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               0,  # deblock-filter
                               1,  # prefix-nal
                               45,  # idr-interval
                               ]
            elif resolution == 'WXGA':
                self.config = [47,  # gop
                               2474,  # bitrate
                               35,  # ip-period
                               37,  # init-qp
                               24,  # qpmin
                               25,  # qpmax
                               0,  # disable-frame-skip
                               7,  # diff-qp-ip
                               21,  # diff-qp-ib
                               9,  # num-ref-frame
                               2,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               0,  # deblock-filter
                               1,  # prefix-nal
                               45,  # idr-interval
                               ]
            elif resolution == 'KITTI':
                self.config = [47,  # gop
                               2474,  # bitrate
                               35,  # ip-period
                               37,  # init-qp
                               24,  # qpmin
                               25,  # qpmax
                               0,  # disable-frame-skip
                               7,  # diff-qp-ip
                               21,  # diff-qp-ib
                               9,  # num-ref-frame
                               2,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               0,  # deblock-filter
                               1,  # prefix-nal
                               45,  # idr-interval
                               ]
            elif resolution == 'FHD':
                self.config = [47,  # gop
                               2474,  # bitrate
                               35,  # ip-period
                               37,  # init-qp
                               24,  # qpmin
                               25,  # qpmax
                               0,  # disable-frame-skip
                               7,  # diff-qp-ip
                               21,  # diff-qp-ib
                               9,  # num-ref-frame
                               2,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               0,  # deblock-filter
                               1,  # prefix-nal
                               45,  # idr-interval
                               ]
            elif resolution == 'QXGA':
                self.config = [47,  # gop
                               2474,  # bitrate
                               35,  # ip-period
                               37,  # init-qp
                               24,  # qpmin
                               25,  # qpmax
                               0,  # disable-frame-skip
                               7,  # diff-qp-ip
                               21,  # diff-qp-ib
                               9,  # num-ref-frame
                               2,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               0,  # deblock-filter
                               1,  # prefix-nal
                               45,  # idr-interval
                               ]

        ################################################### QSV-VP9 ####################################################
        if encoder == QSV_VP9.TAG:
            if resolution == 'VGA':
                self.config = [250,  # gop
                               5000,  # bitrate
                               0,  # ip-period
                               51,  # init-qp
                               0,  # qpmin
                               0,  # qpmax
                               0,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               16,  # num-ref-frame
                               2,  # rc-mode
                               1,  # reference-mode
                               ]
            elif resolution == 'SVGA':
                self.config = [149,  # gop
                               3247,  # bitrate
                               10,  # ip-period
                               2,  # init-qp
                               20,  # qpmin
                               51,  # qpmax
                               1,  # disable-frame-skip
                               0,  # diff-qp-ip
                               14,  # diff-qp-ib
                               14,  # num-ref-frame
                               1,  # rc-mode
                               0,  # reference-mode
                               ]
            elif resolution == 'XGA':
                self.config = [109,  # gop
                               3399,  # bitrate
                               12,  # ip-period
                               20,  # init-qp
                               27,  # qpmin
                               32,  # qpmax
                               0,  # disable-frame-skip
                               23,  # diff-qp-ip
                               1,  # diff-qp-ib
                               1,  # num-ref-frame
                               1,  # rc-mode
                               1,  # reference-mode
                               ]
            elif resolution == 'WXGA':
                self.config = [10,  # gop
                               2000,  # bitrate
                               0,  # ip-period
                               26,  # init-qp
                               1,  # qpmin
                               51,  # qpmax
                               0,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               1,  # num-ref-frame
                               4,  # rc-mode
                               0,  # reference-mode
                               ]
            elif resolution == 'KITTI':
                self.config = [10,  # gop
                               2000,  # bitrate
                               0,  # ip-period
                               26,  # init-qp
                               1,  # qpmin
                               51,  # qpmax
                               0,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               1,  # num-ref-frame
                               4,  # rc-mode
                               0,  # reference-mode
                               ]
            elif resolution == 'FHD':
                self.config = [10,  # gop
                               2000,  # bitrate
                               0,  # ip-period
                               26,  # init-qp
                               1,  # qpmin
                               51,  # qpmax
                               0,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               1,  # num-ref-frame
                               4,  # rc-mode
                               0,  # reference-mode
                               ]
            elif resolution == 'QXGA':
                self.config = [189,  # gop
                               3540,  # bitrate
                               15,  # ip-period
                               44,  # init-qp
                               29,  # qpmin
                               6,  # qpmax
                               0,  # disable-frame-skip
                               24,  # diff-qp-ip
                               19,  # diff-qp-ib
                               9,  # num-ref-frame
                               2,  # rc-mode
                               1,  # reference-mode
                               ]


class COPPLAR:
    def __init__(self, resolution, encoder):
        self.config = None

        ##################################################### VP9 ######################################################
        if encoder == VP9.TAG:
            if resolution == 'VGA':
                self.config = [26,  # gop
                               67,  # drop_frame
                               0,  # resize_allowed
                               87,  # resize_up
                               30,  # resize_down
                               22,  # undershoot_pct
                               85,  # overshoot_pct
                               17,  # min_q
                               1,  # end_usage
                               3264,  # buffer_size
                               3268,  # buffer_init_size
                               3519,  # buffer_optimal_size
                               2168373,  # bitrate
                               1,  # kf_mode
                               0,  # kf_min_dist
                               93,  # kf_max_dist
                               8  # cpu_used
                               ]

            elif resolution == 'SVGA':
                self.config = [159,  # gop
                               0,  # drop_frame
                               1,  # resize_allowed
                               0,  # resize_up
                               93,  # resize_down
                               95,  # undershoot_pct
                               16,  # overshoot_pct
                               13,  # min_q
                               0,  # end_usage
                               6000,  # buffer_size
                               1147,  # buffer_init_size
                               0,  # buffer_optimal_size
                               3895523,  # bitrate
                               1,  # kf_mode
                               1,  # kf_min_dist
                               163,  # kf_max_dist
                               9  # cpu_used
                               ]
            elif resolution == 'XGA':
                self.config = [68,  # gop
                               18,  # drop_frame
                               1,  # resize_allowed
                               90,  # resize_up
                               100,  # resize_down
                               31,  # undershoot_pct
                               31,  # overshoot_pct
                               44,  # min_q
                               1,  # end_usage
                               5425,  # buffer_size
                               4000,  # buffer_init_size
                               1445,  # buffer_optimal_size
                               2194015,  # bitrate
                               0,  # kf_mode
                               0,  # kf_min_dist
                               173,  # kf_max_dist
                               6  # cpu_used
                               ]
            elif resolution == 'WXGA':
                self.config = [243,  # gop
                               0,  # drop_frame
                               1,  # resize_allowed
                               73,  # resize_up
                               28,  # resize_down
                               20,  # undershoot_pct
                               0,  # overshoot_pct
                               26,  # min_q
                               0,  # end_usage
                               0,  # buffer_size
                               0,  # buffer_init_size
                               3275,  # buffer_optimal_size
                               3559766,  # bitrate
                               1,  # kf_mode
                               0,  # kf_min_dist
                               0,  # kf_max_dist
                               8  # cpu_used
                               ]
            elif resolution == 'KITTI':
                self.config = [250,  # gop
                               0,  # drop_frame
                               0,  # resize_allowed
                               100,  # resize_up
                               100,  # resize_down
                               100,  # undershoot_pct
                               0,  # overshoot_pct
                               41,  # min_q
                               1,  # end_usage
                               6000,  # buffer_size
                               444,  # buffer_init_size
                               3547,  # buffer_optimal_size
                               5000000,  # bitrate
                               0,  # kf_mode
                               0,  # kf_min_dist
                               250,  # kf_max_dist
                               6  # cpu_used
                               ]
            elif resolution == 'FHD':
                self.config = [250,  # gop
                               0,  # drop_frame
                               0,  # resize_allowed
                               100,  # resize_up
                               100,  # resize_down
                               100,  # undershoot_pct
                               0,  # overshoot_pct
                               41,  # min_q
                               1,  # end_usage
                               6000,  # buffer_size
                               444,  # buffer_init_size
                               3547,  # buffer_optimal_size
                               5000000,  # bitrate
                               0,  # kf_mode
                               0,  # kf_min_dist
                               250,  # kf_max_dist
                               16  # cpu_used
                               ]
            elif resolution == 'QXGA':
                self.config = [250,  # gop
                               0,  # drop_frame
                               0,  # resize_allowed
                               100,  # resize_up
                               100,  # resize_down
                               100,  # undershoot_pct
                               0,  # overshoot_pct
                               41,  # min_q
                               1,  # end_usage
                               6000,  # buffer_size
                               444,  # buffer_init_size
                               3547,  # buffer_optimal_size
                               5000000,  # bitrate
                               0,  # kf_mode
                               0,  # kf_min_dist
                               250,  # kf_max_dist
                               16  # cpu_used
                               ]

        ##################################################### H264 #####################################################
        if encoder == H264.TAG:
            if resolution == 'VGA':
                self.config = [446583,  # bitrate
                               100000,  # max_bitrate
                               250,  # qop
                               0,  # rc_mode
                               0,  # ecomplexity
                               0,  # sps_pps_strategy
                               16,  # num_ref_frame
                               1,  # ssei
                               0,  # prefix_nal
                               1,  # entropy_coding
                               1,  # frame_skip
                               0,  # qp_max
                               50,  # qp_min
                               0,  # long_term_ref
                               2,  # loop_filter
                               0,  # denoise
                               0,  # background_detection
                               1,  # adaptive_quant
                               1,  # frame_cropping
                               0,  # scene_change_detect
                               1]  # padding

            elif resolution == 'SVGA':
                self.config = [4753765,  # bitrate
                               1938988,  # max_bitrate
                               144,  # qop
                               0,  # rc_mode
                               0,  # ecomplexity
                               0,  # sps_pps_strategy
                               1,  # num_ref_frame
                               0,  # ssei
                               1,  # prefix_nal
                               0,  # entropy_coding
                               1,  # frame_skip
                               41,  # qp_max
                               0,  # qp_min
                               1,  # long_term_ref
                               0,  # loop_filter
                               0,  # denoise
                               1,  # background_detection
                               1,  # adaptive_quant
                               1,  # frame_cropping
                               0,  # scene_change_detect
                               1  # padding
                               ]
            elif resolution == 'XGA':
                self.config = [5000000,  # bitrate
                               100000,  # max_bitrate
                               250,  # qop
                               0,  # rc_mode
                               0,  # ecomplexity
                               3,  # sps_pps_strategy
                               1,  # num_ref_frame
                               0,  # ssei
                               1,  # prefix_nal
                               1,  # entropy_coding
                               0,  # frame_skip
                               0,  # qp_max
                               50,  # qp_min
                               1,  # long_term_ref
                               2,  # loop_filter
                               1,  # denoise
                               0,  # background_detection
                               0,  # adaptive_quant
                               1,  # frame_cropping
                               0,  # scene_change_detect
                               0  # padding
                               ]
            elif resolution == 'WXGA':
                self.config = [100000,  # bitrate
                               100000,  # max_bitrate
                               250,  # qop
                               0,  # rc_mode
                               0,  # ecomplexity
                               1,  # sps_pps_strategy
                               1,  # num_ref_frame
                               0,  # ssei
                               1,  # prefix_nal
                               0,  # entropy_coding
                               1,  # frame_skip
                               0,  # qp_max
                               0,  # qp_min
                               0,  # long_term_ref
                               2,  # loop_filter
                               0,  # denoise
                               0,  # background_detection
                               1,  # adaptive_quant
                               0,  # frame_cropping
                               0,  # scene_change_detect
                               0,  # padding
                               ]
            elif resolution == 'KITTI':
                self.config = [5000000,  # bitrate
                               194700,  # max_bitrate
                               250,  # qop
                               0,  # rc_mode
                               2,  # ecomplexity
                               2,  # sps_pps_strategy
                               1,  # num_ref_frame
                               1,  # ssei
                               1,  # prefix_nal
                               0,  # entropy_coding
                               1,  # frame_skip
                               0,  # qp_max
                               50,  # qp_min
                               1,  # long_term_ref
                               0,  # loop_filter
                               1,  # denoise
                               0,  # background_detection
                               1,  # adaptive_quant
                               0,  # frame_cropping
                               1,  # scene_change_detect
                               0  # padding
                               ]
            elif resolution == 'FHD':
                self.config = [1500000,  # bitrate
                               5000000,  # max_bitrate
                               10,  # qop
                               0,  # rc_mode
                               0,  # ecomplexity
                               0,  # sps_pps_strategy
                               1,  # num_ref_frame
                               0,  # ssei
                               0,  # prefix_nal
                               0,  # entropy_coding
                               1,  # frame_skip
                               42,  # qp_max
                               12,  # qp_min
                               0,  # long_term_ref
                               0,  # loop_filter
                               0,  # denoise
                               1,  # background_detection
                               1,  # adaptive_quant
                               1,  # frame_cropping
                               1,  # scene_change_detect
                               1  # padding
                               ]
            elif resolution == 'QXGA':
                self.config = [1778179,  # bitrate
                               2551222,  # max_bitrate
                               230,  # qop
                               2,  # rc_mode
                               0,  # ecomplexity
                               1,  # sps_pps_strategy
                               3,  # num_ref_frame
                               1,  # ssei
                               0,  # prefix_nal
                               1,  # entropy_coding
                               1,  # frame_skip
                               39,  # qp_max
                               40,  # qp_min
                               0,  # long_term_ref
                               0,  # loop_filter
                               1,  # denoise
                               0,  # background_detection
                               1,  # adaptive_quant
                               0,  # frame_cropping
                               0,  # scene_change_detect
                               1  # padding
                               ]

        ################################################### QSV-H264 ###################################################
        if encoder == QSV_H264.TAG:
            if resolution == 'VGA':
                self.config = [160,  # gop
                               2868,  # bitrate
                               20,  # ip-period
                               25,  # init-qp
                               1,  # qpmin
                               25,  # qpmax
                               0,  # disable-frame-skip
                               12,  # diff-qp-ip
                               31,  # diff-qp-ib
                               10,  # num-ref-frame
                               1,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               1,  # dct8x8
                               0,  # deblock-filter
                               0,  # prefix-nal
                               31,  # idr-interval
                               ]
            elif resolution == 'SVGA':
                self.config = [225,  # gop
                               2253,  # bitrate
                               35,  # ip-period
                               13,  # init-qp
                               27,  # qpmin
                               41,  # qpmax
                               1,  # disable-frame-skip
                               20,  # diff-qp-ip
                               17,  # diff-qp-ib
                               11,  # num-ref-frame
                               3,  # rc-mode
                               1,  # profile
                               1,  # cabac
                               1,  # dct8x8
                               0,  # deblock-filter
                               0,  # prefix-nal
                               22,  # idr-interval
                               ]
            elif resolution == 'XGA':
                self.config = [47,  # gop
                               2474,  # bitrate
                               35,  # ip-period
                               37,  # init-qp
                               24,  # qpmin
                               25,  # qpmax
                               0,  # disable-frame-skip
                               7,  # diff-qp-ip
                               21,  # diff-qp-ib
                               9,  # num-ref-frame
                               2,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               0,  # deblock-filter
                               1,  # prefix-nal
                               45,  # idr-interval
                               ]
            elif resolution == 'WXGA':
                self.config = [47,  # gop
                               2474,  # bitrate
                               35,  # ip-period
                               37,  # init-qp
                               24,  # qpmin
                               25,  # qpmax
                               0,  # disable-frame-skip
                               7,  # diff-qp-ip
                               21,  # diff-qp-ib
                               9,  # num-ref-frame
                               2,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               0,  # deblock-filter
                               1,  # prefix-nal
                               45,  # idr-interval
                               ]
            elif resolution == 'KITTI':
                self.config = [47,  # gop
                               2474,  # bitrate
                               35,  # ip-period
                               37,  # init-qp
                               24,  # qpmin
                               25,  # qpmax
                               0,  # disable-frame-skip
                               7,  # diff-qp-ip
                               21,  # diff-qp-ib
                               9,  # num-ref-frame
                               2,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               0,  # deblock-filter
                               1,  # prefix-nal
                               45,  # idr-interval
                               ]
            elif resolution == 'FHD':
                self.config = [47,  # gop
                               2474,  # bitrate
                               35,  # ip-period
                               37,  # init-qp
                               24,  # qpmin
                               25,  # qpmax
                               0,  # disable-frame-skip
                               7,  # diff-qp-ip
                               21,  # diff-qp-ib
                               9,  # num-ref-frame
                               2,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               0,  # deblock-filter
                               1,  # prefix-nal
                               45,  # idr-interval
                               ]
            elif resolution == 'QXGA':
                self.config = [47,  # gop
                               2474,  # bitrate
                               35,  # ip-period
                               37,  # init-qp
                               24,  # qpmin
                               25,  # qpmax
                               0,  # disable-frame-skip
                               7,  # diff-qp-ip
                               21,  # diff-qp-ib
                               9,  # num-ref-frame
                               2,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               0,  # deblock-filter
                               1,  # prefix-nal
                               45,  # idr-interval
                               ]

        ################################################### QSV-VP9 ####################################################
        if encoder == QSV_VP9.TAG:
            if resolution == 'VGA':
                self.config = [250,  # gop
                               5000,  # bitrate
                               0,  # ip-period
                               51,  # init-qp
                               0,  # qpmin
                               0,  # qpmax
                               0,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               16,  # num-ref-frame
                               2,  # rc-mode
                               1,  # reference-mode
                               ]
            elif resolution == 'SVGA':
                self.config = [149,  # gop
                               3247,  # bitrate
                               10,  # ip-period
                               2,  # init-qp
                               20,  # qpmin
                               51,  # qpmax
                               1,  # disable-frame-skip
                               0,  # diff-qp-ip
                               14,  # diff-qp-ib
                               14,  # num-ref-frame
                               1,  # rc-mode
                               0,  # reference-mode
                               ]
            elif resolution == 'XGA':
                self.config = [109,  # gop
                               3399,  # bitrate
                               12,  # ip-period
                               20,  # init-qp
                               27,  # qpmin
                               32,  # qpmax
                               0,  # disable-frame-skip
                               23,  # diff-qp-ip
                               1,  # diff-qp-ib
                               1,  # num-ref-frame
                               1,  # rc-mode
                               1,  # reference-mode
                               ]
            elif resolution == 'WXGA':
                self.config = [10,  # gop
                               2000,  # bitrate
                               0,  # ip-period
                               26,  # init-qp
                               1,  # qpmin
                               51,  # qpmax
                               0,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               1,  # num-ref-frame
                               4,  # rc-mode
                               0,  # reference-mode
                               ]
            elif resolution == 'KITTI':
                self.config = [10,  # gop
                               2000,  # bitrate
                               0,  # ip-period
                               26,  # init-qp
                               1,  # qpmin
                               51,  # qpmax
                               0,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               1,  # num-ref-frame
                               4,  # rc-mode
                               0,  # reference-mode
                               ]
            elif resolution == 'FHD':
                self.config = [10,  # gop
                               2000,  # bitrate
                               0,  # ip-period
                               26,  # init-qp
                               1,  # qpmin
                               51,  # qpmax
                               0,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               1,  # num-ref-frame
                               4,  # rc-mode
                               0,  # reference-mode
                               ]
            elif resolution == 'QXGA':
                self.config = [189,  # gop
                               3540,  # bitrate
                               15,  # ip-period
                               44,  # init-qp
                               29,  # qpmin
                               6,  # qpmax
                               0,  # disable-frame-skip
                               24,  # diff-qp-ip
                               19,  # diff-qp-ib
                               9,  # num-ref-frame
                               2,  # rc-mode
                               1,  # reference-mode
                               ]
