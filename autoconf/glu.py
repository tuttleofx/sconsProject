from _external import *
from gl import *

glu = LibWithHeaderChecker(
		'GLU' if not windows else 'GLU32',
		['GL/glu.h'],
		'c',
		dependencies=[gl]
	)

