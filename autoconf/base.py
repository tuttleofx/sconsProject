from SCons import Variables
from SCons import Environment

import os
import sys
windows = os.name.lower() == "nt" and sys.platform.lower().startswith("win")
unix = not windows

class BaseLibChecker(object):
    '''
    Base class for lib checkers.
    '''
    error        = ''
    name         = 'name-empty'
    libname      = 'libname-empty'
    language     = 'c'
    dependencies = []
    checkDone    = False

    def enabled(self,env,option=None):
        '''
        Return if "option" is in the environment. If "option" is None return if the current library is enabled.
        '''
        if not option:
            option = 'with_'+self.name
        if option in env :
            return env['with_'+self.name]
        return False

    def initOptions(self, putois, opts):
        '''
        Init options for enable/disable or configure the library.
        '''
        raise NotImplementedError

    def configure(self, putois, env):
        '''
        Ta add things to the environment.
        '''
        # putois.printEnv( env, keys=[ 'with_'+self.name, 'incdir_'+self.name, 'libdir_'+self.name, ] )
        if not self.enabled(env):
            return True
        #env.ParseConfig('pkg-config --cflags --libs ' + self.libname)

        if self.enabled(env,'incdir_'+self.name):
            #if self.language == 'c++':
            env.AppendUnique( CPPPATH=env['incdir_'+self.name] )
            if self.language == 'c':
                env.AppendUnique( CPATH=env['incdir_'+self.name] )

        if self.enabled(env,'libdir_'+self.name):
            env.AppendUnique( LIBPATH=env['libdir_'+self.name] )

        return True
        
    def postconfigure(self, putois, env):
        '''
        Particular case, which allow to add things after all libraries checks.
        '''
        return True

    def check(self, conf):
        '''
        This function needs to be reimplemented in sub-classes to check the current library.
        Return True if the library was found, False otherwise.
        '''
        if not self.enabled(conf.env):
            return True
        self.checkDone = True
        return True
    
    def CheckLibWithHeader( self, conf, libname, header, language, call=False ):
        #assert istype( libname, list )
        #assert istype( header,  list )
        if conf.env['check_libs'] and not self.checkDone:
            if isinstance(libname, list) and len(libname) > 1:
                conf.env.Append( LIBS = libname[1:] )
		libname = libname[0]
            return conf.CheckLibWithHeader( libname, header, language=language, call=call )
        else:
            conf.env.Append( LIBS = libname )
            #print 'no CheckLibWithHeader', self.name
            return True
    
    def CheckLib( self, conf, libname ):
        if conf.env['check_libs'] and not self.checkDone:
            if isinstance(libname, list) and len(libname) > 1:
                conf.env.Append( LIBS = libname[:-1] )
		libname = libname[0]
            return conf.CheckLib( libname )
        else:
            conf.env.Append( LIBS = libname )
            #print 'no CheckLib', self.name
            return True
    
    def CheckHeader( self, conf, header, language ):
        if conf.env['check_libs'] and not self.checkDone:
            return conf.CheckHeader( header, language=language )
        else:
            #print 'no CheckHeader', self.name
            return True



class LibWithHeaderChecker(BaseLibChecker):

    def __init__(self, libname, header, language, name=None, call=None, dependencies=[], defines=[] ):
        self.libname  = libname
        self.header   = header
        self.language = language
        self.call = call
        if not name:
            self.name = libname
        else:
            self.name = name
        self.dependencies = dependencies
        self.defines = defines

    def initOptions(self, putois, opts):
        opts.Add( Variables.BoolVariable( 'with_'+self.name,   'enabled compilation with '+self.name, True  ) )
        opts.Add( 'incdir_'+self.name, 'Include directories for '+self.name,  None )
        opts.Add( 'libdir_'+self.name, 'Link directories for '+self.name,     None )
        return True

    def check(self, conf):
        if not self.enabled(conf.env):
            return True
        conf.env.Append( CPPDEFINES = self.defines )
        result = self.CheckLibWithHeader( conf, self.libname, self.header, self.language, call=self.call )
        self.checkDone = True
        #print 'checkDone LibWithHeaderChecker: ', result
        return result


class LibChecker(BaseLibChecker):

    def __init__(self, libname, name=None, dependencies=[], defines=[] ):
        if not name:
            self.name = libname
        else:
            self.name = name
        self.libname = libname
        self.dependencies = dependencies
        self.defines = defines

    def initOptions(self, putois, opts):
        opts.Add( Variables.BoolVariable( 'with_'+self.name, 'enabled compilation with '+self.name, True  ) )
        opts.Add( 'libdir_'+self.name, 'Link directories for '+self.name, None )
        opts.Add( 'incdir_'+self.name, 'Include directory for '+self.name,   None )
        return True

    def check(self, conf):
        if not self.enabled(conf.env):
            return True
        conf.env.Append( CPPDEFINES = self.defines )
        result = self.CheckLib( conf, self.libname )
        self.checkDone = True
        #print 'checkDone LibChecker: ', result
        return result


class HeaderChecker(BaseLibChecker):

    def __init__(self, name, header, language, dependencies=[], libs=[], defines=[]):
        self.name = name
        self.header   = header
        self.language = language
        self.dependencies = dependencies
        self.defines = defines
        self.libs = libs

    def initOptions(self, putois, opts):
        opts.Add( Variables.BoolVariable( 'with_'+self.name,   'enable compilation with '+self.name, True ) )
        opts.Add( 'incdir_'+self.name, 'Include directory for '+self.name,   None )
        if self.libs:
            opts.Add( 'libdir_'+self.name,  'Link directories for '+self.name, None )
        return True

    def postconfigure(self, putois, env):
        '''
        Particular case, which allow to add things after all libraries checks.
        '''
        env.Append( LIBS = self.libs )
	return True

    def check(self, conf):
        if not self.enabled(conf.env):
            return True
        conf.env.Append( CPPDEFINES = self.defines )
        result = self.CheckHeader( conf, self.header, language=self.language )
        self.checkDone = True
        #print 'checkDone HeaderChecker: ', result
        return result


