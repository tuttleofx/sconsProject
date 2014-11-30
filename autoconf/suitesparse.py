from _external import *

suitesparse = LibWithHeaderChecker(['amd','btf','camd','ccolamd','cholmod','colamd','cxsparse','klu','ldl','spqr','umfpack'],
['amd.h','btf.h','colamd.h','SuiteSparse_config.h','btf.h','camd.h','ccolamd.h','cholmod.h','cs.h','SuiteSparseQR.hpp','klu.h','ldl.h','umfpack.h','spqr.hpp'], 'c++', name='suitesparse')
