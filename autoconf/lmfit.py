########################
# lmfit - C/C++ library for Levenberg-Marquardt least-squares minimization and curve fitting
# http://joachimwuttke.de/lmfit/
########################
# download it
# run ./configure [--prefix=<path/to/install>]
# make [install]
# 
# EXAMPLE
# ./configure --prefix=/home/simone/MOOV3D/libs/lmfit/build
# make install

# inside the .sconf
# extern = <the libraries path>
# incdir_lmfit = [ join(extern, 'lmfit/build/include/') ]
# libdir_lmfit = [ join(extern, 'lmfit/build/lib/') ]

from _external import *

lmfit = LibWithHeaderChecker(['lmmin'],['lmcurve.h','lmmin.h'], 'c', name='lmfit')
