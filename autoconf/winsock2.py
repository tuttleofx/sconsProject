from _external import *

winsock2 = LibWithHeaderChecker( 'ws2_32',
		                ['winsock2.h'],
				'c',
				name='winsock2' )
