from _external import *
from m import *
if not windows:
    from gomp import *
from lcms import *


if windows:
	tmpDep = [
			m,			
			lcms,
		]
else:
	tmpDep = [
			m,
			gomp,
			lcms,
		]

raw = LibWithHeaderChecker(
		'raw',
		'libraw/libraw.h',
		'c',
		dependencies = tmpDep
	)

