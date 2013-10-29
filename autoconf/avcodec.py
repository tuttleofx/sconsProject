from _external import *
from avutil import *

avcodec = LibWithHeaderChecker(
				'avcodec',
				'libavcodec/avcodec.h',
				'c',
				dependencies=[avutil]
			)
