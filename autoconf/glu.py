from _external import *
from gl import *

glu = LibWithHeaderChecker('GLU', ['GL/glu.h'], 'c', dependencies=[gl])

