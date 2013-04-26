from _external import *
from gl import *

if windows:
    glu = LibWithHeaderChecker('GLU32', ['windows.h','GL/glu.h'], 'c', dependencies=[gl])   
else : 
    glu = LibWithHeaderChecker('GLU', ['GL/glu.h'], 'c', dependencies=[gl])