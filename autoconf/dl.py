from _external import *

if windows:
    dl = LibWithHeaderChecker('Kernel32', ['windows.h'], 'c')
else:
    dl = LibWithHeaderChecker('dl', ['dlfcn.h'], 'c')


