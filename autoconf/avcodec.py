from _external import *
from avutil import *
from z import *
from x264 import *
# from xavs import *
from lame import *
from bz2 import *
from xvid import *

avcodec = LibWithHeaderChecker(
		'avcodec',
		'libavcodec/avcodec.h',
		'c',
		dependencies=[
			avutil,
			z,
			x264,
			# xavs,
			lame,
			bz2,
			xvid]
		)
