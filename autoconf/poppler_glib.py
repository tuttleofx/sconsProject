from _external import *
from glib import *
from gobject import *
from cairo import *
from freetype import *
from lcms import *
from tiff import *
from jpeg import *
from png import *
from fontconfig import *

poppler_glib = LibWithHeaderChecker('poppler_glib','poppler/glib/poppler.h','c',
	dependencies=[
		glib,
		gobject,
		cairo,
		freetype,
		lcms,
		tiff,
		jpeg,
		png,
		fontconfig,
		] )


