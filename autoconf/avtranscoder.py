from _external import *
from ffmpeg import ffmpeg

avtranscoder = LibWithHeaderChecker(
				'avtranscoder',
				'AvTranscoder/common.hpp',
				'c++',
				dependencies=[ffmpeg]
			)
