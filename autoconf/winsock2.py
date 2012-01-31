from _external import *

winsock2 = LibWithHeaderChecker( 'winsock2',
		                ['winsock2.h'],
				'c',
				name='ws2_32' )
