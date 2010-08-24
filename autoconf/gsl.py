from _external import *
from gslcblas import *
from blas import *

gsl = LibWithHeaderChecker( 'gsl',
                            'gsl/gsl_sys.h',
                            'c',
                            dependencies=[gslcblas, blas],
                           )


