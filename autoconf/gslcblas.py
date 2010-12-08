from _external import *

gslcblas = LibWithHeaderChecker('gslcblas',
                                'gsl/gsl_sys.h',
                                'c',
                                name='gslcblas',
                                dependencies=[blas]
)


