from _external import *
from boost import *
from boost_regex import *

boost_graph = LibWithHeaderChecker( 'boost_graph', 'boost/graph/adjacency_list.hpp', 'c++',
                                    dependencies=[boost, boost_regex] )


