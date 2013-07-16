from _external import *
from gl import *
from glu import *

if macos:
	# freeglut only supports X11: use standard GLUT framework instead
	freeglut = LibWithHeaderChecker(
		'GLUT',
		['GLUT/glut.h'],
		'c',
		name='freeglut'
	)
else:
	freeglut = LibWithHeaderChecker(
		'glut',
		['GL/freeglut.h'],
		'c',
		dependencies=[gl,glu]
	)

