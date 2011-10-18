from _external import *

newmat = LibChecker('newmat')
optpp = LibWithHeaderChecker(
		'opt',
		['OPT++_config.h'],
		'c++',
		name = 'optpp',
		dependencies = [newmat],
	)

