from _external import *
from boost import *
from boost_date_time import *
from boost_chrono import *
from boost_thread import *
from boost_filesystem import *
from rt import *

boost_log = LibWithHeaderChecker(
	'boost_log',
	['boost/log/core.hpp'],
	'c++',
	dependencies = [
		boost,
		boost_date_time,
		boost_chrono,
		boost_thread,
		boost_filesystem,
		rt,
		] )
