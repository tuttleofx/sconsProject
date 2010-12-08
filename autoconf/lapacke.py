from _external import *
from blas import *
from lapack import *

lapacke = LibWithHeaderChecker( ['lapacke'],
                                ['lapacke.h'],
                                'c',
                                name='lapacke',
								dependencies=[blas,lapack])

