from _external import *
from z import *

caca = LibWithHeaderChecker( 'caca',
                             'caca.h',
                             'c',
                             dependencies=[z]
                            )
