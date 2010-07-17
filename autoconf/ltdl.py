from _external import *

if windows:
    ltdl = LibWithHeaderChecker('Kernel32', ['windows.h'], 'c')
else:
    ltdl = LibWithHeaderChecker('ltdl', ['ltdl.h'], 'c')


