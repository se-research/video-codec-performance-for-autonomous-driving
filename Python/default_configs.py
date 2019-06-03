import VP9
import H264
import QSV_VP9
import QSV_H264


# Returns default config for the specific dataset, encoder and resolution. If aforementioned combination
# is absent in DefaultConfigs, None is return and no default config is used to initialize the optimization.
class DefaultConfigs:
    def __init__(self, encoder, dataset, resolution):
        #self.config = None

        self.config = UniversalConfig(resolution, encoder).config

        '''
        if dataset == 'KITTI_DRIVE_0071':
            self.config = KITTI_DRIVE_0071(resolution, encoder).config
        elif dataset == '2019-03-22-AstaZero-RuralRoad':
            self.config = AstaZero_RuralRoad(resolution, encoder).config
        elif dataset == '2019-04-17-COPPLAR':
            self.config = COPPLAR(resolution, encoder).config
        else:
            print('No default config found for the dataset, encoder and resolution')
            self.config = None
        '''


class UniversalConfig:
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
                               1  # padding
                               ]
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
                               0  # padding
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
                               31  # idr-interval
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
                               22  # idr-interval
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
                               45  # idr-interval
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
                               45  # idr-interval
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
                               45  # idr-interval
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
                               45  # idr-interval
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
                               45  # idr-interval
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


class KITTI_DRIVE_0071:
    def __init__(self, resolution, encoder):
        self.config = None

        if resolution == 'KITTI':
            if encoder == VP9.TAG:
                self.config = [152,  # gop
                               84,  # drop_frame
                               0,  # resize_allowed
                               67,  # resize_up
                               64,  # resize_down
                               32,  # undershoot_pct
                               64,  # overshoot_pct
                               41,  # min_q
                               1,  # end_usage
                               5720,  # buffer_size
                               515,  # buffer_init_size
                               2174,  # buffer_optimal_size
                               4257676,  # bitrate
                               0,  # kf_mode
                               0,  # kf_min_dist
                               20,  # kf_max_dist
                               6  # cpu_used
                               ]

            elif encoder == H264.TAG:
                self.config = [2115789,  # bitrate
                               4678119,  # max_bitrate
                               97,  # qop
                               0,  # rc_mode
                               1,  # ecomplexity
                               2,  # sps_pps_strategy
                               3,  # num_ref_frame
                               0,  # ssei
                               0,  # prefix_nal
                               1,  # entropy_coding
                               1,  # frame_skip
                               38,  # qp_max
                               25,  # qp_min
                               0,  # long_term_ref
                               0,  # loop_filter
                               1,  # denoise
                               0,  # background_detection
                               1,  # adaptive_quant
                               0,  # frame_cropping
                               1,  # scene_change_detect
                               1,  # padding
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
                self.config = [128,  # gop
                               50,  # drop_frame
                               0,  # resize_allowed
                               89,  # resize_up
                               68,  # resize_down
                               28,  # undershoot_pct
                               85,  # overshoot_pct
                               12,  # min_q
                               1,  # end_usage
                               5439,  # buffer_size
                               1108,  # buffer_init_size
                               3672,  # buffer_optimal_size
                               4651913,  # bitrate
                               1,  # kf_mode
                               0,  # kf_min_dist
                               21,  # kf_max_dist
                               8  # cpu_used
                               ]
            elif resolution == 'SVGA':
                self.config = [119,  # gop
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
                self.config = [158,  # gop
                               60,  # drop_frame
                               0,  # resize_allowed
                               12,  # resize_up
                               69,  # resize_down
                               56,  # undershoot_pct
                               35,  # overshoot_pct
                               42,  # min_q
                               1,  # end_usage
                               1617,  # buffer_size
                               2355,  # buffer_init_size
                               3070,  # buffer_optimal_size
                               1110211,  # bitrate
                               0,  # kf_mode
                               0,  # kf_min_dist
                               73,  # kf_max_dist
                               8  # cpu_used
                               ]
            elif resolution == 'WXGA':
                self.config = [72,  # gop
                               29,  # drop_frame
                               0,  # resize_allowed
                               36,  # resize_up
                               98,  # resize_down
                               83,  # undershoot_pct
                               44,  # overshoot_pct
                               29,  # min_q
                               0,  # end_usage
                               4661,  # buffer_size
                               3748,  # buffer_init_size
                               82,  # buffer_optimal_size
                               4861404,  # bitrate
                               1,  # kf_mode
                               0,  # kf_min_dist
                               215,  # kf_max_dist
                               8  # cpu_used
                               ]
            elif resolution == 'KITTI':
                self.config = [1,  # gop
                               100,  # drop_frame
                               1,  # resize_allowed
                               21,  # resize_up
                               55,  # resize_down
                               0,  # undershoot_pct
                               100,  # overshoot_pct
                               18,  # min_q
                               1,  # end_usage
                               1670,  # buffer_size
                               4000,  # buffer_init_size
                               1996,  # buffer_optimal_size
                               4338090,  # bitrate
                               1,  # kf_mode
                               0,  # kf_min_dist
                               250,  # kf_max_dist
                               8  # cpu_used
                               ]
            elif resolution == 'FHD':
                self.config = [199,  # gop
                               46,  # drop_frame
                               1,  # resize_allowed
                               84,  # resize_up
                               21,  # resize_down
                               23,  # undershoot_pct
                               78,  # overshoot_pct
                               32,  # min_q
                               1,  # end_usage
                               5109,  # buffer_size
                               666,  # buffer_init_size
                               3288,  # buffer_optimal_size
                               4398511,  # bitrate
                               0,  # kf_mode
                               1,  # kf_min_dist
                               211,  # kf_max_dist
                               9  # cpu_used
                               ]
            elif resolution == 'QXGA':
                self.config = [199,  # gop
                               46,  # drop_frame
                               1,  # resize_allowed
                               84,  # resize_up
                               21,  # resize_down
                               23,  # undershoot_pct
                               78,  # overshoot_pct
                               32,  # min_q
                               1,  # end_usage
                               5109,  # buffer_size
                               666,  # buffer_init_size
                               3288,  # buffer_optimal_size
                               4398511,  # bitrate
                               0,  # kf_mode
                               1,  # kf_min_dist
                               211,  # kf_max_dist
                               9  # cpu_used
                               ]

        ##################################################### H264 #####################################################
        if encoder == H264.TAG:
            if resolution == 'VGA':
                self.config = [5000000,  # bitrate
                               5000000,  # max_bitrate
                               250,  # qop
                               4,  # rc_mode
                               0,  # ecomplexity
                               3,  # sps_pps_strategy
                               1,  # num_ref_frame
                               1,  # ssei
                               0,  # prefix_nal
                               1,  # entropy_coding
                               0,  # frame_skip
                               51,  # qp_max
                               50,  # qp_min
                               0,  # long_term_ref
                               2,  # loop_filter
                               1,  # denoise
                               0,  # background_detection
                               0,  # adaptive_quant
                               1,  # frame_cropping
                               1,  # scene_change_detect
                               0]  # padding

            elif resolution == 'SVGA':
                self.config = [100000,  # bitrate
                               100000,  # max_bitrate
                               250,  # qop
                               0,  # rc_mode
                               1,  # ecomplexity
                               1,  # sps_pps_strategy
                               16,  # num_ref_frame
                               0,  # ssei
                               1,  # prefix_nal
                               0,  # entropy_coding
                               0,  # frame_skip
                               0,  # qp_max
                               0,  # qp_min
                               1,  # long_term_ref
                               0,  # loop_filter
                               0,  # denoise
                               0,  # background_detection
                               1,  # adaptive_quant
                               1,  # frame_cropping
                               1,  # scene_change_detect
                               1  # padding
                               ]
            elif resolution == 'XGA':
                self.config = [100000,  # bitrate
                               5000000,  # max_bitrate
                               1,  # qop
                               1,  # rc_mode
                               0,  # ecomplexity
                               1,  # sps_pps_strategy
                               11,  # num_ref_frame
                               0,  # ssei
                               0,  # prefix_nal
                               0,  # entropy_coding
                               1,  # frame_skip
                               36,  # qp_max
                               0,  # qp_min
                               0,  # long_term_ref
                               2,  # loop_filter
                               0,  # denoise
                               1,  # background_detection
                               1,  # adaptive_quant
                               0,  # frame_cropping
                               0,  # scene_change_detect
                               1  # padding
                               ]
            elif resolution == 'WXGA':
                self.config = [100000,  # bitrate
                               100000,  # max_bitrate
                               250,  # qop
                               0,  # rc_mode
                               1,  # ecomplexity
                               2,  # sps_pps_strategy
                               16,  # num_ref_frame
                               0,  # ssei
                               0,  # prefix_nal
                               1,  # entropy_coding
                               0,  # frame_skip
                               0,  # qp_max
                               50,  # qp_min
                               1,  # long_term_ref
                               2,  # loop_filter
                               0,  # denoise
                               1,  # background_detection
                               1,  # adaptive_quant
                               1,  # frame_cropping
                               1,  # scene_change_detect
                               0  # padding
                               ]
            elif resolution == 'KITTI':
                self.config = [576675,  # bitrate
                               1988781,  # max_bitrate
                               3,  # qop
                               1,  # rc_mode
                               0,  # ecomplexity
                               2,  # sps_pps_strategy
                               11,  # num_ref_frame
                               1,  # ssei
                               0,  # prefix_nal
                               1,  # entropy_coding
                               0,  # frame_skip
                               0,  # qp_max
                               37,  # qp_min
                               0,  # long_term_ref
                               0,  # loop_filter
                               0,  # denoise
                               0,  # background_detection
                               0,  # adaptive_quant
                               1,  # frame_cropping
                               1,  # scene_change_detect
                               0  # padding
                               ]
            elif resolution == 'FHD':
                self.config = [333439,  # bitrate
                               333439,  # max_bitrate
                               60,  # qop
                               3,  # rc_mode
                               1,  # ecomplexity
                               3,  # sps_pps_strategy
                               14,  # num_ref_frame
                               0,  # ssei
                               1,  # prefix_nal
                               1,  # entropy_coding
                               0,  # frame_skip
                               38,  # qp_max
                               19,  # qp_min
                               1,  # long_term_ref
                               0,  # loop_filter
                               1,  # denoise
                               1,  # background_detection
                               0,  # adaptive_quant
                               0,  # frame_cropping
                               1,  # scene_change_detect
                               1  # padding
                               ]
            elif resolution == 'QXGA':
                self.config = [3545512,  # bitrate
                               3927599,  # max_bitrate
                               44,  # qop
                               2,  # rc_mode
                               1,  # ecomplexity
                               2,  # sps_pps_strategy
                               4,  # num_ref_frame
                               1,  # ssei
                               1,  # prefix_nal
                               1,  # entropy_coding
                               1,  # frame_skip
                               39,  # qp_max
                               19,  # qp_min
                               1,  # long_term_ref
                               0,  # loop_filter
                               0,  # denoise
                               0,  # background_detection
                               1,  # adaptive_quant
                               0,  # frame_cropping
                               0,  # scene_change_detect
                               1  # padding
                               ]

        ################################################### QSV-H264 ###################################################
        if encoder == QSV_H264.TAG:
            if resolution == 'VGA':
                self.config = [18,  # gop
                               918,  # bitrate
                               47,  # ip-period
                               45,  # init-qp
                               1,  # qpmin
                               3,  # qpmax
                               0,  # disable-frame-skip
                               6,  # diff-qp-ip
                               3,  # diff-qp-ib
                               11,  # num-ref-frame
                               3,  # rc-mode
                               1,  # profile
                               1,  # cabac
                               1,  # dct8x8
                               1,  # deblock-filter
                               1,  # prefix-nal
                               6  # idr-interval
                               ]
            elif resolution == 'SVGA':
                self.config = [15,  # gop
                               1039,  # bitrate
                               3,  # ip-period
                               40,  # init-qp
                               40,  # qpmin
                               6,  # qpmax
                               0,  # disable-frame-skip
                               29,  # diff-qp-ip
                               16,  # diff-qp-ib
                               16,  # num-ref-frame
                               2,  # rc-mode
                               1,  # profile
                               1,  # cabac
                               1,  # dct8x8
                               0,  # deblock-filter
                               0,  # prefix-nal
                               1  # idr-interval
                               ]
            elif resolution == 'XGA':
                self.config = [158,  # gop
                               1398,  # bitrate
                               50,  # ip-period
                               48,  # init-qp
                               47,  # qpmin
                               32,  # qpmax
                               0,  # disable-frame-skip
                               41,  # diff-qp-ip
                               50,  # diff-qp-ib
                               4,  # num-ref-frame
                               0,  # rc-mode
                               1,  # profile
                               1,  # cabac
                               1,  # dct8x8
                               1,  # deblock-filter
                               1,  # prefix-nal
                               5  # idr-interval
                               ]
            elif resolution == 'WXGA':
                self.config = [1,  # gop
                               5000,  # bitrate
                               0,  # ip-period
                               0,  # init-qp
                               0,  # qpmin
                               51,  # qpmax
                               1,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               16,  # num-ref-frame
                               0,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               1,  # deblock-filter
                               1,  # prefix-nal
                               50  # idr-interval
                               ]
            elif resolution == 'KITTI':
                self.config = [1,  # gop
                               5000,  # bitrate
                               0,  # ip-period
                               0,  # init-qp
                               0,  # qpmin
                               51,  # qpmax
                               1,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               16,  # num-ref-frame
                               0,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               1,  # deblock-filter
                               1,  # prefix-nal
                               50  # idr-interval
                               ]
            elif resolution == 'FHD':
                self.config = [1,  # gop
                               5000,  # bitrate
                               0,  # ip-period
                               0,  # init-qp
                               0,  # qpmin
                               51,  # qpmax
                               1,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               16,  # num-ref-frame
                               0,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               1,  # deblock-filter
                               1,  # prefix-nal
                               50  # idr-interval
                               ]
            elif resolution == 'QXGA':
                self.config = [1,  # gop
                               5000,  # bitrate
                               0,  # ip-period
                               0,  # init-qp
                               0,  # qpmin
                               51,  # qpmax
                               1,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               16,  # num-ref-frame
                               0,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               1,  # deblock-filter
                               1,  # prefix-nal
                               50  # idr-interval
                               ]

        ################################################### QSV-VP9 ####################################################
        if encoder == QSV_VP9.TAG:
            if resolution == 'VGA':
                self.config = [72,  # gop
                               4809,  # bitrate
                               34,  # ip-period
                               51,  # init-qp
                               30,  # qpmin
                               51,  # qpmax
                               0,  # disable-frame-skip
                               17,  # diff-qp-ip
                               35,  # diff-qp-ib
                               0,  # num-ref-frame
                               3,  # rc-mode
                               1,  # reference-mode
                               ]
            elif resolution == 'SVGA':
                self.config = [12,  # gop
                               4084,  # bitrate
                               9,  # ip-period
                               47,  # init-qp
                               27,  # qpmin
                               14,  # qpmax
                               1,  # disable-frame-skip
                               51,  # diff-qp-ip
                               0,  # diff-qp-ib
                               2,  # num-ref-frame
                               4,  # rc-mode
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
                self.config = [117,  # gop
                               3259,  # bitrate
                               41,  # ip-period
                               40,  # init-qp
                               4,  # qpmin
                               42,  # qpmax
                               0,  # disable-frame-skip
                               46,  # diff-qp-ip
                               9,  # diff-qp-ib
                               4,  # num-ref-frame
                               1,  # rc-mode
                               1  # reference-mode
                               ]
            elif resolution == 'KITTI':
                self.config = [117,  # gop
                               3259,  # bitrate
                               41,  # ip-period
                               40,  # init-qp
                               4,  # qpmin
                               42,  # qpmax
                               0,  # disable-frame-skip
                               46,  # diff-qp-ip
                               9,  # diff-qp-ib
                               4,  # num-ref-frame
                               1,  # rc-mode
                               1  # reference-mode
                               ]
            elif resolution == 'FHD':
                self.config = [117,  # gop
                               3259,  # bitrate
                               41,  # ip-period
                               40,  # init-qp
                               4,  # qpmin
                               42,  # qpmax
                               0,  # disable-frame-skip
                               46,  # diff-qp-ip
                               9,  # diff-qp-ib
                               4,  # num-ref-frame
                               1,  # rc-mode
                               1  # reference-mode
                               ]
            elif resolution == 'QXGA':
                self.config = [117,  # gop
                               3259,  # bitrate
                               41,  # ip-period
                               40,  # init-qp
                               4,  # qpmin
                               42,  # qpmax
                               0,  # disable-frame-skip
                               46,  # diff-qp-ip
                               9,  # diff-qp-ib
                               4,  # num-ref-frame
                               1,  # rc-mode
                               1  # reference-mode
                               ]


class COPPLAR:
    def __init__(self, resolution, encoder):
        self.config = None

        ##################################################### VP9 ######################################################
        if encoder == VP9.TAG:
            if resolution == 'VGA':
                self.config = [100,  # gop
                               0,  # drop_frame
                               1,  # resize_allowed
                               96,  # resize_up
                               4,  # resize_down
                               54,  # undershoot_pct
                               27,  # overshoot_pct
                               0,  # min_q
                               1,  # end_usage
                               220,  # buffer_size
                               1846,  # buffer_init_size
                               676,  # buffer_optimal_size
                               5000000,  # bitrate
                               0,  # kf_mode
                               0,  # kf_min_dist
                               239,  # kf_max_dist
                               7  # cpu_used
                               ]
            elif resolution == 'SVGA':
                self.config = [50,  # gop
                               56,  # drop_frame
                               1,  # resize_allowed
                               0,  # resize_up
                               67,  # resize_down
                               20,  # undershoot_pct
                               92,  # overshoot_pct
                               4,  # min_q
                               1,  # end_usage
                               261,  # buffer_size
                               1865,  # buffer_init_size
                               1951,  # buffer_optimal_size
                               3540857,  # bitrate
                               0,  # kf_mode
                               1,  # kf_min_dist
                               214,  # kf_max_dist
                               6  # cpu_used
                               ]
            elif resolution == 'XGA':
                self.config = [72,  # gop
                               38,  # drop_frame
                               1,  # resize_allowed
                               4,  # resize_up
                               36,  # resize_down
                               83,  # undershoot_pct
                               41,  # overshoot_pct
                               15,  # min_q
                               1,  # end_usage
                               2558,  # buffer_size
                               3351,  # buffer_init_size
                               4497,  # buffer_optimal_size
                               2638630,  # bitrate
                               1,  # kf_mode
                               0,  # kf_min_dist
                               201,  # kf_max_dist
                               7  # cpu_used
                               ]
            elif resolution == 'WXGA':
                self.config = [170,  # gop
                               50,  # drop_frame
                               1,  # resize_allowed
                               31,  # resize_up
                               67,  # resize_down
                               50,  # undershoot_pct
                               28,  # overshoot_pct
                               14,  # min_q
                               1,  # end_usage
                               3091,  # buffer_size
                               3504,  # buffer_init_size
                               2885,  # buffer_optimal_size
                               4731717,  # bitrate
                               1,  # kf_mode
                               1,  # kf_min_dist
                               203,  # kf_max_dist
                               9  # cpu_used
                               ]
            elif resolution == 'KITTI':
                self.config = [165,  # gop
                               51,  # drop_frame
                               0,  # resize_allowed
                               57,  # resize_up
                               19,  # resize_down
                               55,  # undershoot_pct
                               30,  # overshoot_pct
                               13,  # min_q
                               0,  # end_usage
                               2906,  # buffer_size
                               3982,  # buffer_init_size
                               3820,  # buffer_optimal_size
                               2599699,  # bitrate
                               0,  # kf_mode
                               1,  # kf_min_dist
                               94,  # kf_max_dist
                               5  # cpu_used
                               ]
            elif resolution == 'FHD':
                self.config = [224,  # gop
                               2,  # drop_frame
                               0,  # resize_allowed
                               31,  # resize_up
                               33,  # resize_down
                               75,  # undershoot_pct
                               90,  # overshoot_pct
                               6,  # min_q
                               0,  # end_usage
                               3703,  # buffer_size
                               139,  # buffer_init_size
                               3583,  # buffer_optimal_size
                               1301562,  # bitrate
                               1,  # kf_mode
                               0,  # kf_min_dist
                               56,  # kf_max_dist
                               9  # cpu_used
                               ]
            elif resolution == 'QXGA':
                self.config = [224,  # gop
                               2,  # drop_frame
                               0,  # resize_allowed
                               31,  # resize_up
                               33,  # resize_down
                               75,  # undershoot_pct
                               90,  # overshoot_pct
                               6,  # min_q
                               0,  # end_usage
                               3703,  # buffer_size
                               139,  # buffer_init_size
                               3583,  # buffer_optimal_size
                               1301562,  # bitrate
                               1,  # kf_mode
                               0,  # kf_min_dist
                               56,  # kf_max_dist
                               9  # cpu_used
                               ]

        ##################################################### H264 #####################################################
        if encoder == H264.TAG:
            if resolution == 'VGA':
                self.config = [1659381,  # bitrate
                               3105912,  # max_bitrate
                               121,  # qop
                               2,  # rc_mode
                               2,  # ecomplexity
                               1,  # sps_pps_strategy
                               8,  # num_ref_frame
                               1,  # ssei
                               0,  # prefix_nal
                               1,  # entropy_coding
                               1,  # frame_skip
                               6,  # qp_max
                               15,  # qp_min
                               0,  # long_term_ref
                               0,  # loop_filter
                               1,  # denoise
                               1,  # background_detection
                               1,  # adaptive_quant
                               1,  # frame_cropping
                               0,  # scene_change_detect
                               1]  # padding
            elif resolution == 'SVGA':
                self.config = [2868693,  # bitrate
                               3450438,  # max_bitrate
                               195,  # qop
                               1,  # rc_mode
                               1,  # ecomplexity
                               1,  # sps_pps_strategy
                               12,  # num_ref_frame
                               0,  # ssei
                               0,  # prefix_nal
                               1,  # entropy_coding
                               1,  # frame_skip
                               16,  # qp_max
                               48,  # qp_min
                               0,  # long_term_ref
                               0,  # loop_filter
                               1,  # denoise
                               1,  # background_detection
                               1,  # adaptive_quant
                               1,  # frame_cropping
                               1,  # scene_change_detect
                               0  # padding
                               ]
            elif resolution == 'XGA':
                self.config = [1741255,  # bitrate
                               1895495,  # max_bitrate
                               250,  # qop
                               1,  # rc_mode
                               1,  # ecomplexity
                               6,  # sps_pps_strategy
                               16,  # num_ref_frame
                               1,  # ssei
                               1,  # prefix_nal
                               1,  # entropy_coding
                               0,  # frame_skip
                               0,  # qp_max
                               0,  # qp_min
                               1,  # long_term_ref
                               0,  # loop_filter
                               1,  # denoise
                               1,  # background_detection
                               0,  # adaptive_quant
                               1,  # frame_cropping
                               1,  # scene_change_detect
                               1  # padding
                               ]
            elif resolution == 'WXGA':
                self.config = [5000000,  # bitrate
                               5000000,  # max_bitrate
                               250,  # qop
                               1,  # rc_mode
                               2,  # ecomplexity
                               3,  # sps_pps_strategy
                               8,  # num_ref_frame
                               1,  # ssei
                               0,  # prefix_nal
                               1,  # entropy_coding
                               0,  # frame_skip
                               0,  # qp_max
                               37,  # qp_min
                               0,  # long_term_ref
                               1,  # loop_filter
                               0,  # denoise
                               1,  # background_detection
                               0,  # adaptive_quant
                               0,  # frame_cropping
                               1,  # scene_change_detect
                               0  # padding
                               ]
            elif resolution == 'KITTI':
                self.config = [1324609,  # bitrate
                               2870508,  # max_bitrate
                               14,  # qop
                               3,  # rc_mode
                               0,  # ecomplexity
                               0,  # sps_pps_strategy
                               3,  # num_ref_frame
                               1,  # ssei
                               0,  # prefix_nal
                               0,  # entropy_coding
                               0,  # frame_skip
                               21,  # qp_max
                               12,  # qp_min
                               0,  # long_term_ref
                               1,  # loop_filter
                               1,  # denoise
                               0,  # background_detection
                               1,  # adaptive_quant
                               0,  # frame_cropping
                               1,  # scene_change_detect
                               0  # padding
                               ]
            elif resolution == 'FHD':
                self.config = [919706,  # bitrate
                               3316137,  # max_bitrate
                               81,  # qop
                               2,  # rc_mode
                               1,  # ecomplexity
                               3,  # sps_pps_strategy
                               8,  # num_ref_frame
                               0,  # ssei
                               0,  # prefix_nal
                               0,  # entropy_coding
                               1,  # frame_skip
                               32,  # qp_max
                               45,  # qp_min
                               0,  # long_term_ref
                               1,  # loop_filter
                               1,  # denoise
                               1,  # background_detection
                               0,  # adaptive_quant
                               1,  # frame_cropping
                               0,  # scene_change_detect
                               0  # padding
                               ]
            elif resolution == 'QXGA':
                self.config = [1392802,  # bitrate
                               2462543,  # max_bitrate
                               157,  # qop
                               2,  # rc_mode
                               1,  # ecomplexity
                               1,  # sps_pps_strategy
                               15,  # num_ref_frame
                               0,  # ssei
                               0,  # prefix_nal
                               0,  # entropy_coding
                               1,  # frame_skip
                               37,  # qp_max
                               50,  # qp_min
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
                self.config = [11,  # gop
                               4999,  # bitrate
                               29,  # ip-period
                               5,  # init-qp
                               48,  # qpmin
                               2,  # qpmax
                               1,  # disable-frame-skip
                               34,  # diff-qp-ip
                               12,  # diff-qp-ib
                               1,  # num-ref-frame
                               2,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               1,  # dct8x8
                               0,  # deblock-filter
                               0,  # prefix-nal
                               47  # idr-interval
                               ]
            elif resolution == 'SVGA':
                self.config = [250,  # gop
                               5000,  # bitrate
                               0,  # ip-period
                               0,  # init-qp
                               50,  # qpmin
                               0,  # qpmax
                               0,  # disable-frame-skip
                               0,  # diff-qp-ip
                               51,  # diff-qp-ib
                               16,  # num-ref-frame
                               0,  # rc-mode
                               0,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               1,  # deblock-filter
                               0,  # prefix-nal
                               50  # idr-interval
                               ]
            elif resolution == 'XGA':
                self.config = [138,  # gop
                               5000,  # bitrate
                               0,  # ip-period
                               51,  # init-qp
                               0,  # qpmin
                               0,  # qpmax
                               1,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               16,  # num-ref-frame
                               0,  # rc-mode
                               2,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               0,  # deblock-filter
                               1,  # prefix-nal
                               0  # idr-interval
                               ]
            elif resolution == 'WXGA':
                self.config = [208,  # gop
                               1510,  # bitrate
                               15,  # ip-period
                               31,  # init-qp
                               41,  # qpmin
                               8,  # qpmax
                               0,  # disable-frame-skip
                               17,  # diff-qp-ip
                               33,  # diff-qp-ib
                               9,  # num-ref-frame
                               3,  # rc-mode
                               1,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               1,  # deblock-filter
                               1,  # prefix-nal
                               14  # idr-interval
                               ]
            elif resolution == 'KITTI':
                self.config = [208,  # gop
                               1510,  # bitrate
                               15,  # ip-period
                               31,  # init-qp
                               41,  # qpmin
                               8,  # qpmax
                               0,  # disable-frame-skip
                               17,  # diff-qp-ip
                               33,  # diff-qp-ib
                               9,  # num-ref-frame
                               3,  # rc-mode
                               1,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               1,  # deblock-filter
                               1,  # prefix-nal
                               14  # idr-interval
                               ]
            elif resolution == 'FHD':
                self.config = [208,  # gop
                               1510,  # bitrate
                               15,  # ip-period
                               31,  # init-qp
                               41,  # qpmin
                               8,  # qpmax
                               0,  # disable-frame-skip
                               17,  # diff-qp-ip
                               33,  # diff-qp-ib
                               9,  # num-ref-frame
                               3,  # rc-mode
                               1,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               1,  # deblock-filter
                               1,  # prefix-nal
                               14  # idr-interval
                               ]
            elif resolution == 'QXGA':
                self.config = [208,  # gop
                               1510,  # bitrate
                               15,  # ip-period
                               31,  # init-qp
                               41,  # qpmin
                               8,  # qpmax
                               0,  # disable-frame-skip
                               17,  # diff-qp-ip
                               33,  # diff-qp-ib
                               9,  # num-ref-frame
                               3,  # rc-mode
                               1,  # profile
                               1,  # cabac
                               0,  # dct8x8
                               1,  # deblock-filter
                               1,  # prefix-nal
                               14  # idr-interval
                               ]

        ################################################### QSV-VP9 ####################################################
        if encoder == QSV_VP9.TAG:
            if resolution == 'VGA':
                self.config = [250,  # gop
                               5000,  # bitrate
                               50,  # ip-period
                               0,  # init-qp
                               50,  # qpmin
                               51,  # qpmax
                               0,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               0,  # num-ref-frame
                               0,  # rc-mode
                               1  # reference-mode
                               ]
            elif resolution == 'SVGA':
                self.config = [38,  # gop
                               5000,  # bitrate
                               4,  # ip-period
                               51,  # init-qp
                               16,  # qpmin
                               0,  # qpmax
                               1,  # disable-frame-skip
                               0,  # diff-qp-ip
                               0,  # diff-qp-ib
                               0,  # num-ref-frame
                               4,  # rc-mode
                               1  # reference-mode
                               ]
            elif resolution == 'XGA':
                self.config = [111,  # gop
                               4768,  # bitrate
                               34,  # ip-period
                               35,  # init-qp
                               14,  # qpmin
                               37,  # qpmax
                               0,  # disable-frame-skip
                               8,  # diff-qp-ip
                               23,  # diff-qp-ib
                               12,  # num-ref-frame
                               3,  # rc-mode
                               0  # reference-mode
                               ]
            elif resolution == 'WXGA':
                self.config = [24,  # gop
                               3728,  # bitrate
                               25,  # ip-period
                               34,  # init-qp
                               13,  # qpmin
                               9,  # qpmax
                               1,  # disable-frame-skip
                               31,  # diff-qp-ip
                               41,  # diff-qp-ib
                               14,  # num-ref-frame
                               2,  # rc-mode
                               1  # reference-mode
                               ]
            elif resolution == 'KITTI':
                self.config = [24,  # gop
                               3728,  # bitrate
                               25,  # ip-period
                               34,  # init-qp
                               13,  # qpmin
                               9,  # qpmax
                               1,  # disable-frame-skip
                               31,  # diff-qp-ip
                               41,  # diff-qp-ib
                               14,  # num-ref-frame
                               2,  # rc-mode
                               1  # reference-mode
                               ]
            elif resolution == 'FHD':
                self.config = [24,  # gop
                               3728,  # bitrate
                               25,  # ip-period
                               34,  # init-qp
                               13,  # qpmin
                               9,  # qpmax
                               1,  # disable-frame-skip
                               31,  # diff-qp-ip
                               41,  # diff-qp-ib
                               14,  # num-ref-frame
                               2,  # rc-mode
                               1  # reference-mode
                               ]
            elif resolution == 'QXGA':
                self.config = [24,  # gop
                               3728,  # bitrate
                               25,  # ip-period
                               34,  # init-qp
                               13,  # qpmin
                               9,  # qpmax
                               1,  # disable-frame-skip
                               31,  # diff-qp-ip
                               41,  # diff-qp-ib
                               14,  # num-ref-frame
                               2,  # rc-mode
                               1  # reference-mode
                               ]
