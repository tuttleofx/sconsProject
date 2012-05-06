from _external import *
from gl import *
from glu import *

freeglut = LibWithHeaderChecker(
		'freeglut',
		['GL/freeglut.h'],
		'c',
		dependencies=[gl,glu]
	)

