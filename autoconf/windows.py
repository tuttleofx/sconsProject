from _external import *

windows = LibWithHeaderChecker( ['Kernel32','Shell32'],
		                ['windows.h'],
				'c',
				name='windows' )


