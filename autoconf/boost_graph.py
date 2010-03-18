from base import *
from boost import *

boost_graph = LibWithHeaderChecker( 'boost_graph', 'boost/graph/adjacency_list.hpp', 'c++',
                                    dependencies=[boost] )

