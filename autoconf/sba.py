from _external import *
from clapack import *

sba = LibWithHeaderChecker('sba', 'sba.h', 'c', dependencies=[clapack])

