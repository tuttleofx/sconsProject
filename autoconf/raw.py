from _external import *
from m import *
from gomp import *
from lcms import *

raw = LibWithHeaderChecker(
		'raw',
		'libraw/libraw.h',
		'c',
		dependencies = [
			m,
			gomp,
			lcms,
		]
	)

