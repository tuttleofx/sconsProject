from _external import *
from gomp import *
from littlecms import *

raw = LibWithHeaderChecker(
		'raw',
		'libraw/libraw.h',
		'c',
		dependencies = [
			gomp,
			littlecms,
		]
	)

