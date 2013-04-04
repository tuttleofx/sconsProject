from _external import *
from boost import *
from boost_system import *

boost_thread = LibWithHeaderChecker(
	'boost_thread',
	'boost/thread.hpp',
	'c++',
	dependencies=[boost, boost_system]
	)

