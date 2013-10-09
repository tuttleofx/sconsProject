from _external import *
from m import *
from lcms import *

rawDependencies = [
		m,			
		lcms,
	]

if linux:
	from gomp import *
	rawDependencies.append(gomp)


raw = LibWithHeaderChecker(
		'raw',
		'libraw/libraw.h',
		'c',
		dependencies = rawDependencies
	)

