from _external import *

numpy = LibWithHeaderChecker( name='numpy',
                              libs='npymath',
                              header='numpy/numpyconfig.h',
                              language='c')
