from _external import *

if windows:
    qtmain = LibChecker( 'qtmain' )
else:
    qtmain = ObjectChecker( 'qtmain' )

