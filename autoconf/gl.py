from _external import *

if windows:
    gl = LibWithHeaderChecker('opengl32', ['windows.h','GL/gl.h'], 'c', name='gl')
elif macos:
    gl = LibWithHeaderChecker('OpenGL', ['AGL/gl.h'], 'c', name='gl')
else : # unix
    gl = LibWithHeaderChecker('GL', ['GL/gl.h'], 'c', name='gl')


