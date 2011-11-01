from _external import *
from glu import *
from gl import *

libname = 'GLEW'
if windows:
	libname = 'glew32'

glew = LibWithHeaderChecker(
	libname,
	'GL/glew.h',
	'c',
	name='glew',
	dependencies=[glu,gl]
	)


