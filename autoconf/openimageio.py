from _external import *
from boost import *
from dl import *

openimageio = LibWithHeaderChecker(
            ['OpenImageIO'], 'imageio.h', 'c++',
            name='openimageio',
            call='',
            dependencies =[boost,dl] )


