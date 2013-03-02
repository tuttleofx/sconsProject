
name = 'visualc'
ccBin = 'cl'
cxxBin = 'cl'
linkBin = 'link'
linkxxBin = 'link'

ccVersionStr = 'unknown'
ccVersion = [0,0,0]

CC = {}
CC['define']   = '/D'
CC['exceptionsEnabled'] = '/EHsc' #'/GX'

CC['multithreadedlib'] = '/MD'
CC['singlethreadedlib'] = '/ML'

CC['optimize']   =['/O2','/Ox','/GA','/GL']
CC['nooptimize'] =['/Od']
# /O2            Creates fast code
# /Ox            Uses maximum optimization (/Ob2gity /Gs)
# /GA            Optimizes code for Windows application
# /GL            Enables whole program optimization
# /Od            Disables optimization

# /MACHINE:$(PROCESSOR_ARCHITECTURE)
# /GR            Enables run-time type information (RTTI)
# /GX            Enables synchronous exception handling

CC['linkoptimize']   = ['/LTCG'] # associated to /GL flag
CC['linknooptimize'] = ['']

CC['warning1']  = ['/W1']
CC['warning2']  = ['/W2']
CC['warning3']  = ['/W3']
CC['warning4']  = ['/W4']
CC['nowarning'] = ['/w', '/W0']

CC['sharedNoUndefined'] = ['']
CC['visibilityhidden'] = ['']
CC['sharedobject'] = ['']

CC['profile']   = ['/PROFILE']
CC['linkprofile'] = []
CC['cover']     = []
CC['linkcover'] = []


CC['debug'] = ['/DEBUG','/Zi'] + CC['nooptimize']
# /Zi            Generates complete debugging information
# desapprouvee : '/Yd'
CC['linkdebug'] = CC['linknooptimize']

CC['release'] = CC['optimize']
CC['linkrelease'] = CC['linkoptimize']

CC['production'] = CC['optimize']
CC['linkproduction'] = CC['linkoptimize']

# base : recommended in all cases
CC['base']      = [CC['exceptionsEnabled']]
CC['linkbase']  = []


CC['sse']   = ['/arch:SSE']
CC['sse2']  = ['/arch:SSE2']
CC['sse3']  = ['/arch:SSE3']
CC['ssse3'] = ['/arch:SSSE3']
CC['sse4']  = ['/arch:SSE4']


def retrieveVersion(ccBinArg):
    import subprocess
    try:
        # todo
        return 'unknown' #subprocess.Popen( [ccBinArg, CC['version']], stdout=subprocess.PIPE, stderr=subprocess.PIPE  ).communicate()[0].strip()
    except:
        return 'unknown'


def setup(ccBinArg, cxxBinArg):
    global ccVersionStr, ccVersion
    
    ccVersionStr = retrieveVersion(ccBinArg)
    cxxVersionStr = retrieveVersion(cxxBinArg)


