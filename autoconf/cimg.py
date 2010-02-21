from base import *


if windows:
    cimg = LibWithHeaderChecker( ['user32','shell32','gdi32'],['windows.h','CImg.h'], 'c++', name='cimg' )
else:
    cimg = HeaderChecker( 'cimg','CImg.h', 'c++' )

