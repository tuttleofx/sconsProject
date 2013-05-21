
name = 'visualc'
ccBin = 'cl'
cxxBin = 'cl'
linkBin = 'link'
linkxxBin = 'link'


CC = {}
CC['define']   = '/D'
CC['exceptionsEnabled'] = '/EHsc' #'/GX'

CC['multithreadedlib'] = '/MD'
CC['multithreaded_static_lib'] = '/MT'
CC['singlethreadedlib'] = '/ML'
CC['bigobj'] = '/bigobj'

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


CC['debug']   = ['/DEBUG','/Zi'] + CC['nooptimize']
# /Zi            Generates complete debugging information
# desapprouvee : '/Yd'
CC['release']   = CC['optimize']

# base : recommended in all cases
CC['base']      = [CC['exceptionsEnabled']]
CC['linkbase']  = []


CC['sse']   = ['/arch:SSE']
CC['sse2']  = ['/arch:SSE2']
CC['sse3']  = ['/arch:SSE3']
CC['ssse3'] = ['/arch:SSSE3']
CC['sse4']  = ['/arch:SSE4']

def version( bin = 'cl' ):
	import subprocess
	try:
		# todo
		return 'unknown' #subprocess.Popen( [bin], stdout=subprocess.PIPE, stderr=subprocess.PIPE  ).communicate()[0].strip()
	except:
		return 'unknown'
