from _external import *
from z import *
from bz2 import *

ffmpeg = LibWithHeaderChecker(
		[
			'avdevice',
			'swscale',
			'avformat',
			'avcodec',
			'avutil',
			'avfilter',
			'swresample',
		],
		'libavformat/avformat.h',
		'c',
		name='ffmpeg',
		defines=['__STDC_CONSTANT_MACROS'],
		dependencies=[z,bz2]
	)


