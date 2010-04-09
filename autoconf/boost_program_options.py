from _external import *
from boost_system import *
from boost import *

boost_program_options = LibWithHeaderChecker( 'boost_program_options',
                                         'boost/program_options.hpp', 'c++',
                                         dependencies=[boost_system, boost] )

