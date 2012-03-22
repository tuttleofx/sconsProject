from _external import *

opencolorio = LibWithHeaderChecker(
            ['OpenColorIO'], 'OpenColorIO.h', 'c++',
            name='opencolorio',
            call='',
            dependencies =[] )


