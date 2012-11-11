from _external import *
from boost import *

boost_atomic = HeaderChecker(
	'boost_atomic',
	['boost/atomic.hpp'],
	'c++',
	dependencies=[boost] )

