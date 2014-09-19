from _external import *

suitesparse = LibWithHeaderChecker(['amd','btf','camd','ccolamd','cholmod','colamd','cxsparse','klu','ldl','rbio','spqr','ufconfig','umfpack'],
['amd.h','btf.h','colamd.h','RBio.h','SuiteSparse_config.h','btf.h','camd.h','ccolamd.h','cholmod.h','cs.h','SuiteSparseQR','klu.h','ldl.h','umfpack.h','spqr.hpp'], 'c++', name='suitesparse')
