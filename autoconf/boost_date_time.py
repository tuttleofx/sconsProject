from _external import *
from boost_system import *
from boost import *

boost_date_time = LibWithHeaderChecker( 'boost_date_time',
                                         'boost/date_time.hpp', 'c++',
                                         dependencies=[boost] )

