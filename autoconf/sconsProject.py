from _base import *

class SConsProjectChecker(BaseLibChecker):
    '''
    Default configuration.
    '''

    def __init__( self ):
        self.name  = 'sconsProject'
        pass

    def initOptions(self, project, opts):
        self.initOption_with(project, opts)
        return True

    def configure(self, project, env):
        if not self.enabled(env):
            return True
        env.AppendUnique( LIBPATH = [ project.inOutputLib() ] )
        
        env.AppendUnique( CPPSUFFIXES = [ '.tcc' ] )
        # CPPSUFFIXES: The list of suffixes of files that will be scanned for C preprocessor implicit dependencies (#include lines).
        # The default list is [".c", ".C", ".cxx", ".cpp", ".c++", ".cc", ".h", ".H", ".hxx", ".hpp", ".hh", ".F", ".fpp", ".FPP", ".m", ".mm", ".S", ".spp", ".SPP"]

        env.AppendUnique( CCFLAGS = project.CC['base'] )
        env.AppendUnique( LINKFLAGS = project.CC['linkbase'] )
        
        if windows:
            env.AppendUnique( CPPDEFINES = 'WIN' )
            env.AppendUnique( CPPDEFINES = 'WINDOWS' )
            env.AppendUnique( CPPDEFINES = '_WINDOWS' )
            env.AppendUnique( CPPDEFINES = '__WINDOWS__' )
#            env.AppendUnique( CPPDEFINES = 'WIN'+str(env['osbits']) )
        else:
            env.AppendUnique( CPPDEFINES = 'UNIX' )
            env.AppendUnique( CPPDEFINES = '__UNIX__' )
            if macos: # for disabling macros such as check, verify, require ... (AssertMacros.h)
                env.AppendUnique( CPPDEFINES = '__ASSERT_MACROS_DEFINE_VERSIONS_WITHOUT_UNDERSCORES=0')

        if env['mode'] == 'debug' :
            env.AppendUnique( CCFLAGS = project.CC['debug'] )
            env.AppendUnique( CPPDEFINES = 'DEBUG' )
        else :
            env.AppendUnique( CCFLAGS = project.CC['release'] )
            env.AppendUnique( CPPDEFINES = 'NDEBUG' )
            env.AppendUnique( CPPDEFINES = 'RELEASE' )

        if env['mode'] == 'production' :
            env.AppendUnique( CPPDEFINES = 'PRODUCTION' )

        if env['profile'] :
            env.AppendUnique( CCFLAGS = project.CC['profile'] )
            env.AppendUnique( LINKFLAGS = project.CC['linkprofile'] )
            
        if env['cover'] :
            env.AppendUnique( CCFLAGS = project.CC['cover'] )
            env.AppendUnique( LINKFLAGS = project.CC['linkcover'] )
        
        return True


sconsProject = SConsProjectChecker()


