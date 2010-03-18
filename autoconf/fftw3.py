from _external import *

fftw3 = LibWithHeaderChecker('fftw3', 'fftw3.h', 'c', call='fftw_plan p;')


