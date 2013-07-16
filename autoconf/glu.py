from _external import *
from gl import *

if windows:
    glu = LibWithHeaderChecker('GLU32', ['windows.h','GL/glu.h'], 'c', dependencies=[gl])   
if macos:
    glu = LibWithHeaderChecker('OpenGL', ['OpenGL/glu.h'], 'c', name='glu')
else : 
    glu = LibWithHeaderChecker('GLU', ['GL/glu.h'], 'c', dependencies=[gl])
