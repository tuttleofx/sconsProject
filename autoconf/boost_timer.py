from _external import *
from boost import *

boost_timer = LibWithHeaderChecker(
	'boost_timer',
	'boost/timer/timer.hpp',
	'c++',
	dependencies=[boost],
	)

