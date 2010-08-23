from _external import *
from gl import *
from glu import *

nvidiaSDI = LibWithHeaderChecker( ['XNVCtrl', 'anc', 'X11', 'Xxf86vm', 'Xi', 'Xmu'],
                                  ['NVCtrl.h'],
                                  'c',
                                  name='nvidiaSDI',
                                  defines=['GL_GLEXT_PROTOTYPES', 'GLX_GLXEXT_PROTOTYPES'],
                                  dependencies=[gl, glu],
                                 )
