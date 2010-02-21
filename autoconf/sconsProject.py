from base import *

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
        env.Append( LIBPATH = [ putois.inOutputLib() ] )
        
        env.Append( CPPSUFFIXES = [ '.tcc' ] )
        # CPPSUFFIXES: The list of suffixes of files that will be scanned for C preprocessor implicit dependencies (#include lines).
        # The default list is [".c", ".C", ".cxx", ".cpp", ".c++", ".cc", ".h", ".H", ".hxx", ".hpp", ".hh", ".F", ".fpp", ".FPP", ".m", ".mm", ".S", ".spp", ".SPP"]

        env.Append( CCFLAGS = putois.CC['base'] )
        env.Append( LINKFLAGS = putois.CC['linkbase'] )
        
        if env['WINDOWS']:
            env.Append( CCFLAGS = putois.CC['define']+'WIN' )
            env.Append( CCFLAGS = putois.CC['define']+'WINDOWS' )
            env.Append( CCFLAGS = putois.CC['define']+'_WINDOWS' )
            env.Append( CCFLAGS = putois.CC['define']+'__WINDOWS__' )
            env.Append( CCFLAGS = putois.CC['define']+'WIN'+str(env['OSBITS']) )
        else:
            env.Append( CCFLAGS = putois.CC['define']+'UNIX' )
            env.Append( CCFLAGS = putois.CC['define']+'__UNIX__' )
        
        env.Append( CCFLAGS = putois.CC['warning4'] )

        if env['mode'] == 'debug' :
            env.Append( CCFLAGS = putois.CC['debug'] )
            env.Append( CCFLAGS = putois.CC['define']+'DEBUG' )
        else :
            env.Append( CCFLAGS = putois.CC['release'] )
            env.Append( CCFLAGS = putois.CC['define']+'NDEBUG' )
            env.Append( CCFLAGS = putois.CC['define']+'RELEASE' )

        if env['mode'] == 'prod' :
            env.Append( CCFLAGS = putois.CC['define']+'PROD' )
            env.Append( CCFLAGS = putois.CC['define']+'PRODUCTION' )

        if env['profile'] :
            env.Append( CCFLAGS = putois.CC['profile'] )
            env.Append( LINKFLAGS = putois.CC['linkprofile'] )
            
        if env['cover'] :
            env.Append( CCFLAGS = putois.CC['cover'] )
            env.Append( LINKFLAGS = putois.CC['linkcover'] )
        
        return True


sconsProject = SConsProjectChecker()


