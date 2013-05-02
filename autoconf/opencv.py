########################
# OpenCV - Open source Computer Vision
# http://opencv.org/
########################
# download it
# mkdir build
# mkdir build/install
# cd build
# ccmake ..
# [set the options and the install directory, ex. build/install]
# cmake .
# make install -j 8
# run ./configure [--prefix=<path/to/install>]
# make [install]
# 
# inside the .sconf
# extern = <the libraries path>
# incdir_opencv = [ join(extern, 'opencv/build/install/include') ]
# libdir_opencv = join(extern,'opencv/build/install/lib')
# 
# THIS WORKS FOR versions 2.3 <= OpenCV <= 2.4.5.
# for older version you may have to change the list of .so/.lib
# 
# if you are using opencv from git repository it may be troublesome as they are 
# flattening the includes and as yet they don't install compatibility headers
# So in the .sconf you may want to do this workaround
# 
#incdir_opencv = [ 
#				   join(extern, 'opencv/modules/core/include/'),
#                  join(extern, 'opencv/modules/calib3d/include/'),
#                  join(extern, 'opencv/modules/contrib/include/'),
#                  join(extern, 'opencv/modules/features2d/include/'),
#                  join(extern, 'opencv/modules/flann/include/'),
#                  join(extern, 'opencv/modules/gpu/include/'),
#                  join(extern, 'opencv/modules/highgui/include/'),
#                  join(extern, 'opencv/modules/imgproc/include/'),
#                  join(extern, 'opencv/modules/legacy/include/'),
#                  join(extern, 'opencv/modules/ml/include/'),
#                  join(extern, 'opencv/modules/nonfree/include/'),
#                  join(extern, 'opencv/modules/objdetect/include/'),
#                  join(extern, 'opencv/modules/photo/include/'),
#                  join(extern, 'opencv/modules/softcascade/include/'),
#                  join(extern, 'opencv/modules/stitching/include/'),
#                  join(extern, 'opencv/modules/superres/include/'),
#                  join(extern, 'opencv/modules/ts/include/'),
#                  join(extern, 'opencv/modules/video/include/'),
#                  join(extern, 'opencv/modules/videostab/include/'),
#                  join(extern, 'opencv/modules/world/include/'),
#                  join(extern, 'opencv/include'),
#                  join(extern, 'opencv/include/opencv'),
#                 ]
# ie, the include paths should point to the source code module instead of 
# the install directory

from _external import *

opencv = LibWithHeaderChecker([
								'opencv_calib3d', 
								'opencv_core', 
								'opencv_contrib' 
								'opencv_features2d', 
								'opencv_flann', 
								'opencv_gpu', 
								'opencv_highgui', 
								'opencv_imgproc', 
								'opencv_java', 
								'opencv_legacy', 
								'opencv_ml', 
								'opencv_nonfree', 
								'opencv_objdetect', 
								'opencv_photo', 
								'opencv_softcascade', 
								'opencv_ts', 
								'opencv_video', 
								'opencv_videostab', 
								],
                              'opencv/cv.h', 'c', name='opencv')
