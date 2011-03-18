from _external import *

cuda = LibWithHeaderChecker( ['cuda','cudart'], 'cuda.h', 'c', name='cuda')

