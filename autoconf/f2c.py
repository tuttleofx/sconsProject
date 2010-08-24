from _external import *
from m import *

f2c = LibWithHeaderChecker('f2c', ['f2c.h'], 'c', dependencies=[m])
