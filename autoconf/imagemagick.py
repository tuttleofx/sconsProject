from _external import *
from lcms import *
from tiff import *
from freetype import *
from jpeg import *
from xlibs import *
from bz2 import *
from z import *
from m import *
from gomp import *
from pthread import *
from ltdl import *

imagemagick = LibWithHeaderChecker(
        ['Magick++', 'MagickWand', 'MagickCore'],
        ['Magick++.h'],
        'c++',
        name='imagemagick',
        dependencies=[lcms, tiff, freetype, jpeg, xlibs, bz2, z, m, gomp, pthread, ltdl]
        )

