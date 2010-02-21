from base import *

if windows:
    glew = LibWithHeaderChecker('glew32','GL/glew.h','c', name='glew')
else:
    glew = LibWithHeaderChecker('GLEW','GL/glew.h','c',name='glew')


