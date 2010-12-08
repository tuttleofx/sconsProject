from _external import *
from boost import *
from lapack import *

boost_numeric_bindings = HeaderChecker( 'boost_numeric_bindings', ['boost/numeric/bindings/lapack/lapack.hpp'], 'c++',
                                         dependencies=[boost, lapack])
