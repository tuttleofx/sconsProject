from _external import *

if windows:
    freetype = LibWithHeaderChecker('freetype', ['ft2build.h'], 'c')
else:
    from fontconfig import *
    freetype = LibWithHeaderChecker('freetype', 'ft2build.h', 'c', dependencies=[fontconfig] )

