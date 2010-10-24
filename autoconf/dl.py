from _external import *

if windows:
    dl = LibWithHeaderChecker(['Kernel32','Shell32'], ['windows.h'], 'c', name='dl')
else:
    dl = LibWithHeaderChecker('dl', ['dlfcn.h'], 'c')


