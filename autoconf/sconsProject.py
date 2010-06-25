from _base import *

class SConsProjectChecker(BaseLibChecker):
    '''
    Default configuration.
    '''

    def __init__( self ):
        self.name  = 'SConsProject'
        pass

    def initOptions(self, putois, opts):
        opts.Add( Variables.BoolVariable( 'with_'+self.name, 'enabled compilation with '+self.name, True  ) )
        return True

    def configure(self, putois, env):
        if not self.enabled(env):
            return True
        env.AppendUnique( LIBPATH = [ putois.inOutputLib() ] )
        
        env.AppendUnique( CPPSUFFIXES = [ '.tcc' ] )
        # CPPSUFFIXES: The list of suffixes of files that will be scanned for C preprocessor implicit dependencies (#include lines).
        # The default list is [".c", ".C", ".cxx", ".cpp", ".c++", ".cc", ".h", ".H", ".hxx", ".hpp", ".hh", ".F", ".fpp", ".FPP", ".m", ".mm", ".S", ".spp", ".SPP"]

        env.AppendUnique( CCFLAGS = putois.CC['base'] )
        env.AppendUnique( LINKFLAGS = putois.CC['linkbase'] )
        
        if env['WINDOWS']:
            env.AppendUnique( CPPDEFINES = 'WIN' )
            env.AppendUnique( CPPDEFINES = 'WINDOWS' )
            env.AppendUnique( CPPDEFINES = '_WINDOWS' )
            env.AppendUnique( CPPDEFINES = '__WINDOWS__' )
            env.AppendUnique( CPPDEFINES = 'WIN'+str(env['OSBITS']) )
        else:
            env.AppendUnique( CPPDEFINES = 'UNIX' )
            env.AppendUnique( CPPDEFINES = '__UNIX__' )

        if env['mode'] == 'debug' :
            env.AppendUnique( CCFLAGS = putois.CC['debug'] )
            env.AppendUnique( CPPDEFINES = 'DEBUG' )
        else :
            env.AppendUnique( CCFLAGS = putois.CC['release'] )
            env.AppendUnique( CPPDEFINES = 'NDEBUG' )
            env.AppendUnique( CPPDEFINES = 'RELEASE' )

        if env['mode'] == 'production' :
            env.AppendUnique( CPPDEFINES = 'PRODUCTION' )

        if env['profile'] :
            env.AppendUnique( CCFLAGS = putois.CC['profile'] )
            env.AppendUnique( LINKFLAGS = putois.CC['linkprofile'] )
            
        if env['cover'] :
            env.AppendUnique( CCFLAGS = putois.CC['cover'] )
            env.AppendUnique( LINKFLAGS = putois.CC['linkcover'] )
        
        return True


sconsProject = SConsProjectChecker()


