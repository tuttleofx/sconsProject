from _external import *

if not windows:
	util = LibChecker('util')
else:
	util = ObjectChecker('util')
