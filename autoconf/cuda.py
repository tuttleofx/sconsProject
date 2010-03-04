from base import *

cuda = LibWithHeaderChecker( ['cuda','cutil','cudart'], 'cuda/cuda.h', 'c', name='cuda')

