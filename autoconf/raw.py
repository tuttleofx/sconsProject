from _external import *
from m import *
from lcms import *

rawDependencies = [
		m,			
		lcms,
	]

if linux:
	from gomp import *
	from jpeg import *
	rawDependencies.append(gomp)
	rawDependencies.append(jpeg)


raw = LibWithHeaderChecker(
		'raw',
		'libraw/libraw.h',
		'c',
		dependencies = rawDependencies
	)

