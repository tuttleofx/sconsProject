from base import *
from boost import *

boost_serialization = LibWithHeaderChecker( ['boost_serialization', 'boost_wserialization'],
                                            'boost/serialization/serialization.hpp',
                                            'c++',
                                            name = 'boost_serialization',
                                            dependencies=[boost] )

