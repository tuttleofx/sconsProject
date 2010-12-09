from _external import *
from blas import *

gslcblas = LibWithHeaderChecker('gslcblas',
                                'gsl/gsl_sys.h',
                                'c',
                                name='gslcblas',
                                dependencies=[blas]
)


