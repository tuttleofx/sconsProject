from _external import *
from jpeg import *

tiff = LibWithHeaderChecker('tiff',['tiff.h', 'tiffio.h'],'c',call='TIFFGetVersion();', dependencies=[jpeg])

