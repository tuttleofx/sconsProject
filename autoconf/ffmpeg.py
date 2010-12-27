from _external import *
from z import *

ffmpeg = LibWithHeaderChecker( ['avutil',
                                'avformat',
                                'avcodec',
                                'swscale',
                                'avdevice'],
                               'libavformat/avformat.h',
                               'c',
                               name='ffmpeg',
                               defines=['__STDC_CONSTANT_MACROS'],
                               dependencies=[z]
                              )
