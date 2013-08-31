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
	imagemagick = LibWithHeaderChecker(
		['MagickCore'],
		['magick/MagickCore.h'],
		'c',
		name='imagemagick',
		dependencies=[lcms, tiff, freetype, jpeg, bz2, z, m, gomp, pthread, ltdl]
        )
else:
	imagemagick = LibWithHeaderChecker(
		['MagickCore'],
		['magick/MagickCore.h'],
		'c',
		name='imagemagick',
		dependencies=[lcms, tiff, freetype, jpeg, xlibs, bz2, z, m, gomp, pthread, ltdl]
        )



