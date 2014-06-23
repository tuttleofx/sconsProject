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
from webp import *
from xml import *
from ddjvu import *
from lzma import *
from openexr import *

# imagemagick C API

if windows:
    imagemagick = LibWithHeaderChecker(
        ['MagickCore'],
        ['magick/MagickCore.h'],
        'c',
        name='imagemagick',
        #dependencies=[lcms, tiff, freetype, jpeg, xlibs, bz2, z, ltdl]
        )
elif macos:
    # Unfortunately, by default ImageMagick is linked with X11,
    # but it can also be configured/installed without X11 support,
    # which is better for OSX (no need to package X11 with ImageMagick,
    # and no conflict between OpenGL libraries)
    # With MacPorts, ImageMagick should be installed with the +no_x11 variant:
    # sudo port install ImageMagick +no_x11
    imagemagick = LibWithHeaderChecker(
        ['MagickCore'],
        ['magick/MagickCore.h'],
        'c',
        name='imagemagick',
        dependencies=[lcms, tiff, freetype, jpeg, bz2, z, m, pthread, ltdl]
        )
else:
    imagemagick = LibWithHeaderChecker(
        ['MagickCore'],
        ['magick/MagickCore.h'],
        'c',
        name='imagemagick',
        dependencies=[lcms, tiff, freetype, jpeg, xlibs, bz2, z, m, gomp, pthread, ltdl, webp, xml, ddjvu, lzma, openexr]
        )



