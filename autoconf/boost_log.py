from _external import *
from boost import *
from boost_date_time import *
from boost_chrono import *
from rt import *

boost_log = LibWithHeaderChecker(
	'boost_log',
	['boost/log/core.hpp'],
	'c++',
	dependencies = [
		boost,
		boost_date_time,
		boost_chrono,
		rt,
		] )
