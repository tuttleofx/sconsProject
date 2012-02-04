import os
import sys
from _external import *
from winsock2 import *
from boost import *

windows = os.name.lower() == "nt" and sys.platform.lower().startswith("win")
if windows:
	boost_asio = HeaderChecker( 'boost_asio', 'boost/asio.hpp', 'c++', dependencies=[boost, winsock2] )
else:
	boost_asio = HeaderChecker( 'boost_asio', 'boost/asio.hpp', 'c++', dependencies=[boost] )

