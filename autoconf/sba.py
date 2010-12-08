from _external import *
from lapack import *

sba = LibWithHeaderChecker('sba', 'sba.h', 'c', dependencies=[lapack])

