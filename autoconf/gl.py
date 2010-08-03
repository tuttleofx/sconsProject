from _external import *

if windows:
    gl = LibWithHeaderChecker('opengl32', ['windows.h','GL/gl.h'], 'c')
elif macos:
    gl = FrameworkChecker('OpenGL', ['AGL/gl.h'], 'c')
else : # unix
    gl = LibWithHeaderChecker('GL', ['GL/gl.h'], 'c')


