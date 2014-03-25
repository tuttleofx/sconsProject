import os
import sys
import gcc

name = 'clang'
ccBin = 'clang'
cxxBin = 'clang++'
linkBin = ccBin
linkxxBin = cxxBin

# by default, same interface than gcc
CC = dict(gcc.CC)

# "-dumpversion" is a gcc option that still exist on clang for compatibility reasons,
# but it always returns the latest compatible gcc version... which is "4.2.1".
# So use "--version" instead.
CC['version']   = '--version'

# clang doesn't support the GCC debugging symbols flags
CC['debug']   = ['-g'] + CC['nooptimize']

#CC['stdlib'] = ['libc++']

def retrieveVersion( bin = 'clang' ):
    import subprocess
    versionMsg = subprocess.Popen( [bin, CC['version']], stdout=subprocess.PIPE).communicate()[0].strip()
    versionStr = versionMsg.split()[3]
    return versionStr

def setup(ccBinArg, cxxBinArg):
    global ccVersionStr, ccVersion

    ccVersionStr = retrieveVersion(ccBinArg)
    cxxVersionStr = retrieveVersion(cxxBinArg)
    if ccVersionStr != cxxVersionStr:
        print "Warning: CC version and CXX version doesn't match: CC version is %s and CXX version is %s\n" % (ccVersionStr, cxxVersionStr)

    if ccVersionStr != 'unknown':
        ccVersion = [int(i) for i in ccVersionStr.split('.')]

    if ccVersion[0]>=4 and ccVersion[1]>1:
        CC['warning2'].append('-Werror=return-type')
    #    CC['warning2'].append('-Werror=return-local-addr')

    CC['warning3']  = CC['warning2']
    if ccVersion[0]>=4 and ccVersion[1]>1:
        CC['warning3'].append('-Werror=switch')
    if ccVersion[0]>=4 and ccVersion[1]>2:
        CC['warning3'].append('-Werror=enum-compare')

    # "warningX" contains all lower level warnings
    for i in xrange(2, 4):
        CC['warning'+str(i)].extend( CC['warning'+str(i-1)] )

