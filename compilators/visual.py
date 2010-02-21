
CC = {}
CC['define']   = '/D'
CC['exceptionsEnabled'] = '/EHsc' #'/GX'

CC['optimize']   =['/O2','/Ox','/GA','/GL'] # 
CC['nooptimize'] =['/Od']
# /O2            Creates fast code
# /Ox            Uses maximum optimization (/Ob2gity /Gs)
# /GA            Optimizes code for Windows application
# /GL            Enables whole program optimization
# /Od            Disables optimization

# /MACHINE:$(PROCESSOR_ARCHITECTURE)
# /GR            Enables run-time type information (RTTI)
# /GX            Enables synchronous exception handling

CC['warning1']  = '/W1'
CC['warning2']  = '/W2'
CC['warning3']  = '/W3'
CC['warning4']  = '/W4'
CC['nowarning'] = ['/w', '/W0']


CC['sharedobject'] = ''


CC['profile']   = ['/PROFILE']
CC['linkprofile'] = []
CC['cover']     = []
CC['linkcover'] = []


CC['debug']   = ['/DDEBUG','/DEBUG','/Zi'] + CC['nooptimize']
# /Zi            Generates complete debugging information
# desapprouvee : '/Yd'
CC['release']   = ['/DRELEASE'] + CC['optimize']

# base : a toujours mettre
CC['base']      = [CC['exceptionsEnabled']]
CC['linkbase']  = []

