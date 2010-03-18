from _external import *
from boost import *

boost_signals = LibWithHeaderChecker( 'boost_signals', 'boost/signals.hpp', 'c++',
                                      dependencies=[boost] )
