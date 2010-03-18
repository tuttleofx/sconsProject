from _external import *

if windows:
    gl = LibWithHeaderChecker('opengl32', ['windows.h','GL/gl.h'], 'c')
else:
    gl = LibWithHeaderChecker('GL', ['GL/gl.h'], 'c')


