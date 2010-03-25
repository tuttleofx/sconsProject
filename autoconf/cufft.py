from _external import *

cufft = LibWithHeaderChecker('cufft', 'cufft.h', 'c', call='cufftReal r;')
