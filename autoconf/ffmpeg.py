from _external import *
from z import *
from bz2 import *

resampleLibraryName = 'avresample'

if not LibWithHeaderChecker('avresample', 'libavresample/avresample.h', 'c'):
    if LibWithHeaderChecker('swresample', 'libswresample/swresample.h', 'c'):
        resampleLibraryName = 'swresample'

ffmpeg = LibWithHeaderChecker(
		[
			'avdevice',
			'swscale',
			'avformat',
			'avcodec',
			'avutil',
			'avfilter',
			resampleLibraryName,
		],
		'libavformat/avformat.h',
		'c',
		name='ffmpeg',
		defines=['__STDC_CONSTANT_MACROS'],
		dependencies=[z,bz2]
	)


