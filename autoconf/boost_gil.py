from base import *
from boost import *

boost_gil = HeaderChecker( 'boost_gil', ['boost/gil/gil_all.hpp'], 'c++',
                           dependencies=[boost] )
