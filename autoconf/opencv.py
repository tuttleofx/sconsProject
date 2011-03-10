from _external import *
#opencv = LibWithHeaderChecker(['opencv_core', 'opencv_video', 'opencv_calib3d', 'opencv_highgui', 'opencv_imgproc', 'opencv_ml', 'opencv_gpu', 'opencv_ml', 'opencv_contrib'], 'opencv/cv.h', 'c', name='opencv')

opencv = LibWithHeaderChecker(['opencv_core', 'opencv_video', 'opencv_calib3d', 'opencv_highgui', 'opencv_imgproc', 'opencv_ml', 'opencv_ml' ],
                              'opencv/cv.h', 'c', name='opencv')
