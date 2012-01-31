from _external import *
from winsock2 import *
from boost import *

boost_asio = HeaderChecker( 'boost_asio', 'boost/asio.hpp', 'c++', dependencies=[boost, winsock2] )

