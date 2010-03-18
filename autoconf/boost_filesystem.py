from base import *
from boost_system import *
from boost import *

boost_filesystem = LibWithHeaderChecker( 'boost_filesystem',
                                         'boost/filesystem.hpp', 'c++',
                                         dependencies=[boost_system, boost] )

