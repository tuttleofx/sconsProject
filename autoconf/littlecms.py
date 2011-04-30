from _external import *

littlecms = LibWithHeaderChecker(
		'lcms',
		['stdio.h','jpeglib.h'],
		'c',
		name = 'littlecms'
	)
