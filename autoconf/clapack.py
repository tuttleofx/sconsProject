from _external import *

clapack = LibWithHeaderChecker(['lapack','blas','f2c'], ['f2c.h','clapack.h'], 'c', name='clapack')

