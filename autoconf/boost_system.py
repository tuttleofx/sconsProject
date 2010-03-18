from _external import *
from boost import *

boost_system = LibWithHeaderChecker( 'boost_system', 'boost/system/config.hpp', 'c++',
                                     dependencies=[boost] )
