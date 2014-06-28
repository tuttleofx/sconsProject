from _external import *
# from yaml import *
# from tinyxml import *

opencolorio = LibWithHeaderChecker(
            ['OpenColorIO'], 'OpenColorIO/OpenColorIO.h', 'c++',
            name='opencolorio',
            call='',
            # dependencies =[tinyxml, yaml],
        )


