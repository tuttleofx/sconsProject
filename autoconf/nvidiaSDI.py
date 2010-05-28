from _external import *

nvidiaSDI = LibWithHeaderChecker(['XNVCtrl', 'anc', 'X11', 'Xxf86vm', 'Xi', 'Xmu', 'GL', 'GLU'],'NVCtrl.h','c',name='nvidiaSDI',defines=['GL_GLEXT_PROTOTYPES', 'GLX_GLXEXT_PROTOTYPES'])
