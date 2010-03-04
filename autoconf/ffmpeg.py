from base import *

ffmpeg = LibWithHeaderChecker(['avutil', 'avformat', 'avdevice', 'avcodec', 'z'], 'libavformat/avformat.h', 'c', name='ffmpeg')
