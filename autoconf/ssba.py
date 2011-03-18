from _external import *
from glut import *

ssba = LibWithHeaderChecker( ['V3D','ldl','colamd'],
                             'Geometry/v3d_metricbundle.h',
                             'c++',
                             name='ssba',
                             defines=['V3DLIB_ENABLE_SUITESPARSE'],
                             dependencies=[glut] )

