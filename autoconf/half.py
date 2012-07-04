from _external import *
from pthread import *

half = LibWithHeaderChecker(
		['Half'],
		['OpenEXR/half.h'],
		'c++',
		name='half',
		dependencies=[pthread],
	    )

