from base import *

ffmpeg = LibWithHeaderChecker(['avutil', 'avformat', 'avcodec', 'swscale', 'avdevice', 'z'], 'libavformat/avformat.h', 'c', name='ffmpeg')
