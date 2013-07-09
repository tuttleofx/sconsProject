from _external import *
from boost_system import *

boost_chrono = LibWithHeaderChecker(
	'boost_chrono',
	['boost/chrono.hpp'],
	'c++',
	dependencies = [
		boost_system,
		] )
