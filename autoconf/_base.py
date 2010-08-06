from SCons import Variables
from SCons import Environment

from operator import add

import os
import sys
windows = os.name.lower() == "nt" and sys.platform.lower().startswith("win")
macos = sys.platform.lower().startswith("darwin")
linux = not windows and not macos
unix = not windows

def asList(v):
	'''Return v inside a list if not a list.'''
	if isinstance(v, list):
		return v
	return [v]

class BaseLibChecker(object):
	'''
	Base class for lib checkers.
	'''
	error        = ''
	name         = 'name-empty'
	language     = 'c'
	dependencies = []
	checkDone    = False
	libs = []
	sconsNode = None # specific to internal libraries, None by default


	def enabled(self,env,option=None):
		'''
		Return if "option" is in the environment. If "option" is None return if the current library is enabled.
		'''
		if not option:
			option = 'with_'+self.name
		if option in env :
			return env['with_'+self.name]
		return False

	def initOptions(self, project, opts):
		'''
		Init options for enable/disable or configure the library.
		'''
		opts.Add( Variables.BoolVariable( 'with_'+self.name,   'Enable compilation with '+self.name, True ) )
		opts.Add( self.name, 'To customize the libraries names if particular on your platform or compiled version.', self.libs )
		if macos:
			opts.Add( 'fwkdir_'+self.name, 'Framework directory for '+self.name,     None )

	def configure(self, project, env):
		'''
		Add things to the environment.
		'''
		# project.printEnv( env, keys=[ 'with_'+self.name, 'incdir_'+self.name, 'libdir_'+self.name, ] )
		#env.ParseConfig('pkg-config --cflags --libs ' + self.libs)

		env.AppendUnique( CPPDEFINES='with_'+self.name )
		if self.enabled(env,'incdir_'+self.name):
			#if self.language == 'c++':
			env.AppendUnique( CPPPATH=env['incdir_'+self.name] )
			if self.language == 'c':
				env.AppendUnique( CPATH=env['incdir_'+self.name] )

		if self.enabled(env,'libdir_'+self.name):
			env.AppendUnique( LIBPATH=env['libdir_'+self.name] )

		if macos:
			if self.enabled(env,'fwkdir_'+self.name):
				fwkdirs = asList(env['fwkdir_'+self.name])
				fwkFlags = ['-F'+f for f in fwkdirs]
				env.Append( LINKFLAGS=fwkFlags )
				env.Append( CCFLAGS=fwkFlags )

		return True

	def postconfigure(self, project, env):
		'''
		Particular case, which allow to add things after all libraries checks.
		'''
		return True

	def check(self, project, conf):
		'''
		This function needs to be reimplemented in sub-classes to check the current library.
		Return True if the library was found, False otherwise.
		'''
		return True

	def useFramework(self, env):
		if not macos:
			return False
		if 'fwkdir_'+self.name not in env:
			return False
		return env['fwkdir_'+self.name] != None
	
	def getLibs(self, env):
		return env[self.name]

	def privateCheckLibWithHeader( self, conf, libs, header, language, call=False ):
		if conf.env['check_libs'] and not self.checkDone:
			if isinstance(libs, list) and len(libs) > 1:
				conf.env.PrependUnique( LIBS = libs[:-1] )

				libs = libs[-1]
			return conf.CheckLibWithHeader( libs, header, language=language, call=call )
		else:
			conf.env.PrependUnique( LIBS = libs )
			#print 'no CheckLibWithHeader', self.name
			return True

	def privateCheckFrameworkWithHeader( self, conf, framework, header, language, call=False ):
		p_framework = asList(framework)
		fwk = reduce(add, [ ['-framework',f] for f in p_framework], [])
		conf.env.Append( LINKFLAGS = fwk )
		#conf.env.Append( CCFLAGS = fwk ) # ?
		self.privateCheckLibWithHeader( conf, libs=[], header=header, language=language )
		return True

	def privateCheckLib( self, conf, libs ):
		if conf.env['check_libs'] and not self.checkDone:
			if isinstance(libs, list) and len(libs) > 1:
				conf.env.PrependUnique( LIBS =  libs[:-1] )
				libs =  libs[-1]
			return conf.CheckLib(  libs )
		else:
			conf.env.PrependUnique( LIBS =  libs )
			#print 'no CheckLib', self.name
			return True

	def privateCheckFramework( self, conf, framework, language, call=False ):
		p_framework = asList(framework)
		conf.env.Append( LINKFLAGS = reduce(add, [ ['-framework',f] for f in framework], []) )
		self.privateCheckLib( conf, libs=[] )
		return True

	def CheckLibWithHeader( self, conf, libs, header, language, call=False ):
		if self.useFramework(conf.env):
			return self.privateCheckFrameworkWithHeader(conf, libs, header, language, call)
		else:
			return self.privateCheckLibWithHeader(conf, libs, header, language, call)
		
	def CheckLib( self, conf, libs ):
		if self.useFramework(conf.env):
			return self.privateCheckFramework(conf, libs)
		else:
			return self.privateCheckLib(conf, libs)

	def CheckHeader( self, conf, header, language ):
		if conf.env['check_libs'] and not self.checkDone:
			return conf.CheckHeader( header, language=language )
		else:
			#print 'no CheckHeader', self.name
			return True

