from _external import *

optpp = LibWithHeaderChecker(
		['opt', 'newmat'],
		['OPT++_config.h'],
		'c++',
		name = 'optpp',
	)

