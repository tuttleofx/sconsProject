from _external import *
from boost import *

boost_math = LibWithHeaderChecker( ['boost_math_c99',
                                    #'boost_math_c99l',
                                    'boost_math_c99f',
                                    'boost_math_tr1',
                                    #'boost_math_tr1l',
                                    'boost_math_tr1f'], 'boost/math.hpp', 'c++',
                                     name='boost_math', dependencies=[boost] )

