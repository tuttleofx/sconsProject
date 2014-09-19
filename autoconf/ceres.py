from _external import *
from pthread import *
from amd import *
from gomp import *
from lapack import *
from suitesparse import *
from glog import *

ceres = LibWithHeaderChecker('ceres', 'ceres/ceres.h', 'c++', name='ceres', dependencies = [gomp,lapack,suitesparse,amd,pthread,glog],)
