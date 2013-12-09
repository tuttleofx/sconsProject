from _external import *
from poco_xml import *

poco_foundation = LibWithHeaderChecker( 'poco_foundation', ['Poco/Foundation.h'], 'c++', dependencies=[poco_xml] )

