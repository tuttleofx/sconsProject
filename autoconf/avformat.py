from _external import *
from avcodec import *
from avutil import *

avformat = LibWithHeaderChecker(
				'avformat',
				'libavformat/avformat.h',
				'c',
				dependencies=[avcodec, avutil]
			)
