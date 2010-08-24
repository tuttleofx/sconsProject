from _external import *
from glu import *
from gl import *

if windows:
    glew = LibWithHeaderChecker('glew32',
                                'GL/glew.h',
                                'c',
                                name='glew',
                                dependencies=[glu,gl]
                                )
else:
    glew = LibWithHeaderChecker('GLEW',
                                'GL/glew.h',
				'c',
				name='glew',
                                dependencies=[glu,gl]
				)


