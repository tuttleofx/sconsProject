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
            env.AppendUnique( CCFLAGS = putois.CC['define']+'WIN' )
            env.AppendUnique( CCFLAGS = putois.CC['define']+'WINDOWS' )
            env.AppendUnique( CCFLAGS = putois.CC['define']+'_WINDOWS' )
            env.AppendUnique( CCFLAGS = putois.CC['define']+'__WINDOWS__' )
            env.AppendUnique( CCFLAGS = putois.CC['define']+'WIN'+str(env['OSBITS']) )
        else:
            env.AppendUnique( CCFLAGS = putois.CC['define']+'UNIX' )
            env.AppendUnique( CCFLAGS = putois.CC['define']+'__UNIX__' )

        if env['mode'] == 'debug' :
            env.AppendUnique( CCFLAGS = putois.CC['debug'] )
            env.AppendUnique( CCFLAGS = putois.CC['define']+'DEBUG' )
        else :
            env.AppendUnique( CCFLAGS = putois.CC['release'] )
            env.AppendUnique( CCFLAGS = putois.CC['define']+'NDEBUG' )
            env.AppendUnique( CCFLAGS = putois.CC['define']+'RELEASE' )

        if env['mode'] == 'production' :
            env.AppendUnique( CCFLAGS = putois.CC['define']+'PROD' )
            env.AppendUnique( CCFLAGS = putois.CC['define']+'PRODUCTION' )

        if env['profile'] :
            env.AppendUnique( CCFLAGS = putois.CC['profile'] )
            env.AppendUnique( LINKFLAGS = putois.CC['linkprofile'] )
            
        if env['cover'] :
            env.AppendUnique( CCFLAGS = putois.CC['cover'] )
            env.AppendUnique( LINKFLAGS = putois.CC['linkcover'] )
        
        return True


sconsProject = SConsProjectChecker()


