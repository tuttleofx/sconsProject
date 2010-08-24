from _external import *
from gl import *
from glu import *

glut = LibWithHeaderChecker('glut', ['GL/glut.h'], 'c', dependencies=[gl,glu])

