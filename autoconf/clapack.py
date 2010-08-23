from _external import *
from blas import *
from f2c import *

clapack = LibWithHeaderChecker( ['lapack'],
                                ['f2c.h','clapack.h'],
                                'c',
                                name='clapack',
                                dependencies=[blas,f2c]
                               )

