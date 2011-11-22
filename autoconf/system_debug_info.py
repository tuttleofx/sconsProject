from _external import *

name = 'system_debug_info'
if windows:
	system_debug_info = LibWithHeaderChecker(['Dbghelp'], ['Dbghelp.h'], 'c', name=name)
else:
	# nothing needed, create an empty target
	system_debug_info = ObjectChecker(name)


