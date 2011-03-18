from _external import *

tiff = LibWithHeaderChecker('tiff',['tiff.h', 'tiffio.h'],'c',call='TIFFGetVersion();')

