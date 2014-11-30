from _external import *
from newmat import *

optpp = LibWithHeaderChecker(
		'opt',
		['OPT++_config.h'],
		'c++',
		name = 'optpp',
		dependencies = [newmat],
	)

