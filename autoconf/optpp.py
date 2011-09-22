from _external import *

newmat = LibChecker('newmat')
optpp = LibWithHeaderChecker('opt', ['Opt.h'], 'c++', dependencies=[newmat])
