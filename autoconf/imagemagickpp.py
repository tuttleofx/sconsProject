from _external import *
from imagemagick import *

# imagemagick C++ API
imagemagickpp = LibWithHeaderChecker(
        ['Magick++', 'MagickWand'],
        ['magick/MagickCore.h'],
        'c++',
        name='imagemagickpp',
        dependencies=[imagemagick]
        )


