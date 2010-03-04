from base import *

maya = HeaderChecker('maya', 'maya/MGlobal.h', 'c++', libs=['OpenMaya','Foundation','OpenMayaUI','OpenMayaAnim'], defines=['_BOOL','REQUIRE_IOSTREAM', 'UNAME', 'LINUX'])

