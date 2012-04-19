from _external import *

opencolorio = LibWithHeaderChecker(
            ['OpenColorIO'], 'OpenColorIO/OpenColorIO.h', 'c++',
            name='opencolorio',
            call='',
            dependencies =[] )


