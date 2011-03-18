from _external import *
from cuda import *

npp = LibWithHeaderChecker(['npp','UtilNPP64'], 'nppi.h', 'c', dependencies=[cuda] )
