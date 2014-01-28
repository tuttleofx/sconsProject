import os
import sys
windows = os.name.lower() == "nt" and sys.platform.lower().startswith("win")
macos = sys.platform.lower().startswith("darwin")
linux = not windows and not macos
unix = not windows


name = 'gcc'
ccBin = 'gcc'
cxxBin = 'g++'
linkBin = ccBin
linkxxBin = cxxBin
ccVersionStr = 'unknown'
ccVersion = [0,0,0]


CC = {}
CC['version']   = '-dumpversion'


CC['define']   = '-D'

CC['bigobj'] = ''
CC['multithreadedlib'] = ''
CC['multithreaded_static_lib'] = ''
CC['singlethreadedlib'] = ''

CC['optimize'] = ['-O3'] #, '-flto']#,
                  #'-finline-limit=700',
                  #'--param large-function-growth=1000']
# '--param inline-unit-growth=100','--param large-function-growth=1000'
# -finline-limit par defaut 600
CC['nooptimize'] =['-O0']
# -0s : optimise en vitesse mais aussi en taille
# -O9
# -funroll-loops
# -ffast-math
# -malign-double
# -mcpu=pentiumpro
# -march=pentiumpro
# -fomit-frame-pointer
# -O3
# -mcpu=pentiumpro
# -march=pentiumpro
# -fnonnull-objects

CC['linkoptimize'] = [] #['-flto']
CC['linknooptimize'] = []


CC['warning1'] = ['-Wall']
CC['warning2'] = []
CC['warning3'] = []
CC['warning4'] = ['-Wshadow', '-Winline']

CC['nowarning'] = ['-w']


if macos:
    # on macos, the linker is not GNU ld
    CC['sharedNoUndefined'] = ['-Wl,-undefined,error']
else:
    CC['sharedNoUndefined'] = ['-Wl,--no-undefined'] #['-Wl,--no-allow-shlib-undefined','-lld-linux']
CC['visibilityhidden'] = ['-fvisibility=hidden']
if windows:
    # dont need to add fPIC because all code is position independant
    CC['sharedobject'] = []
else:
    CC['sharedobject'] = ['-fPIC']

CC['profile']   = ['-pg']
CC['linkprofile']   = ['-pg']
CC['cover']     = ['-fprofile-arcs', '-ftest-coverage']
CC['linkcover'] = ['-lgcov']

##### -fprofile-arcs
#    Instrument arcs during compilation. For each function of your program, GCC creates a program flow graph, then finds a spanning tree for the graph. Only arcs that are not on the spanning tree have to be instrumented: the compiler adds code to count the number of times that these arcs are executed. When an arc is the only exit or only entrance to a block, the instrumentation code can be added to the block; otherwise, a new basic block must be created to hold the instrumentation code.
#
#    Since not every arc in the program must be instrumented, programs compiled with this option run faster than programs compiled with `-a', which adds instrumentation code to every basic block in the program. The tradeoff: since gcov does not have execution counts for all branches, it must start with the execution counts for the instrumented branches, and then iterate over the program flow graph until the entire graph has been solved. Hence, gcov runs a little more slowly than a program which uses information from `-a'.
#
#    `-fprofile-arcs' also makes it possible to estimate branch probabilities, and to calculate basic block execution counts. In general, basic block execution counts do not give enough information to estimate all branch probabilities. When the compiled program exits, it saves the arc execution counts to a file called `sourcename.da'. Use the compiler option `-fbranch-probabilities' (see section Options that Control Optimization) when recompiling, to optimize using estimated branch probabilities.

##### -ftest-coverage
#    Create data files for the gcov code-coverage utility (see section gcov: a GCC Test Coverage Program). The data file names begin with the name of your source file:
#
#    sourcename.bb
#        A mapping from basic blocks to line numbers, which gcov uses to associate basic block execution counts with line numbers.
#
#    sourcename.bbg
#        A list of all arcs in the program flow graph. This allows gcov to reconstruct the program flow graph, so that it can compute all basic block and arc execution counts from the information in the sourcename.da file (this last file is the output from `-fprofile-arcs'). 

CC['debug']   = ['-g3','-ggdb3','-gstabs3'] + CC['nooptimize']
CC['linkdebug'] = CC['linknooptimize']

CC['release'] = CC['optimize']
CC['linkrelease'] = CC['linkoptimize']

CC['production'] = CC['optimize']
CC['linkproduction'] = CC['linkoptimize']


# -ftemplate-depth-1024: A limit on the template instantiation depth is needed to detect endless recursions during template class instantiation.
# ANSI/ISO C++ conforming programs must not rely on a maximum depth greater than 17 (changed to 1024 in C++11)
CC['base']      = ['-ftemplate-depth-1024']
CC['linkbase']  = []



CC['sse']   = ['-msse']
CC['sse2']  = ['-msse2']
CC['sse3']  = ['-msse3']
CC['ssse3']  = ['-mssse3']
CC['sse4']  = ['-msse4']

def retrieveVersion(ccBinArg):
    import subprocess
    try:
        versionStr = subprocess.Popen( [ccBinArg, CC['version']], stdout=subprocess.PIPE, stderr=subprocess.PIPE ).communicate()[0].strip()
        # print 'gcc version: ', versionStr
        return versionStr
    except:
        return 'unknown'

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



