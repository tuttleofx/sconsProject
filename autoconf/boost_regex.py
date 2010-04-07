from _external import *
from boost import *

boost_regex = LibWithHeaderChecker( 'boost_regex', 'boost/regex.hpp', 'c++',
                                     dependencies=[boost] )

 
