from _external import *
from boost import *
from python import *

boost_python = LibWithHeaderChecker( 'boost_python',
                                     'boost/python.hpp',
                                     'c++',
                                     dependencies=[boost, python] )


