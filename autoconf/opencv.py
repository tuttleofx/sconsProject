from _external import *

opencv = LibWithHeaderChecker(['cv', 'cxcore',  'cvaux', 'highgui','ml'],
                              'opencv/cv.h', 'c', name='opencv')
