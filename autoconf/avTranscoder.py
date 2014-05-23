from _external import *
from ffmpeg import ffmpeg

avTranscoder = LibWithHeaderChecker(
				'AvTranscoder',
				'AvTranscoder/common.hpp',
				'c++',
				dependencies=[ffmpeg]
			)
