import os
import sys
from _external import *
from winsock2 import *
from poco_foundation import *

windows = os.name.lower() == "nt" and sys.platform.lower().startswith("win")
if windows:
	poco_net = LibWithHeaderChecker( 'poco_net', 'Poco/Net/Net.h', 'c++', dependencies=[poco_foundation, winsock2] )
else:
	poco_net = LibWithHeaderChecker( 'poco_net', 'Poco/Net/Net.h', 'c++', dependencies=[poco_foundation] )

