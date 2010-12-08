from _external import *
from blas import *
from lapack import *
from gfortran import *

lapack = LibChecker( 'lapack', dependencies=[gfortran, blas])
