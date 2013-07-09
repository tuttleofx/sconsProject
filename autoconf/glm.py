########################
# GLM: an Alias Wavefront OBJ file library
# http://devernay.free.fr/hacks/glm/
########################
# download it
# run ./configure [--prefix=path/to/install]
# make [install]
# 
# EXAMPLE
# ./configure --prefix=/home/simone/MOOV3D/libs/glm/build
# make install

# inside the .sconf
# extern = <the libraries path>
# incdir_glm = [ join(extern, 'glm/build/include/') ]
# libdir_glm = [ join(extern, 'glm/build/lib/') ]

from _external import *

glm = LibWithHeaderChecker(['glm'], ['glm.h'], 'c', name='glm')
