from _external import *

opencv = LibWithHeaderChecker(['opencv_core', 'opencv_video', 'opencv_calib3d', 'opencv_highgui', 'opencv_imgproc', 'opencv_ml'],
                              'opencv/cv.h', 'c', name='opencv')
