from _external import *

if windows:
	z = LibChecker('zlib')
else:
	z = LibChecker('z')
