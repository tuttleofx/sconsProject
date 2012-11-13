from _external import *
from m import *
from gomp import *
from littlecms import *

raw = LibWithHeaderChecker(
		'raw',
		'libraw/libraw.h',
		'c',
		dependencies = [
			m,
			gomp,
			littlecms,
		]
	)

