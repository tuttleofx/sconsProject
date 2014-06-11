from _external import *

if windows:
    freetype = LibWithHeaderChecker('freetype', ['ft2build.h'], 'c')
else:
    from fontconfig import *
    from z import *
    from bz2 import *
    from png import *
    freetype = LibWithHeaderChecker('freetype',
                                    'ft2build.h',
                                    'c',
                                    dependencies=[fontconfig, png, bz2, z]
                                    )
