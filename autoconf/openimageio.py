from _external import *
from dl import *

openimageio = LibWithHeaderChecker(
            ['OpenImageIO'], 'OpenImageIO/imageio.h', 'c++',
            name='openimageio',
            call='',
            dependencies =[dl] )


