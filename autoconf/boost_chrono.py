from _external import *
from boost import *

boost_chrono = LibWithHeaderChecker(
	'boost_chrono',
	['boost/chrono.hpp'],
	'c++',
	dependencies = [
		boost,
		] )
