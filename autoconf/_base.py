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
	libs = []

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
		opts.Add( Variables.BoolVariable( 'with_'+self.name,   'Enable compilation with '+self.name, True  ) )
		#raise NotImplementedError

	def configure(self, project, env):
		'''
		Add things to the environment.
		'''
		# project.printEnv( env, keys=[ 'with_'+self.name, 'incdir_'+self.name, 'libdir_'+self.name, ] )
		if not self.enabled(env):
			return True
		#env.ParseConfig('pkg-config --cflags --libs ' + self.libname)

		env.AppendUnique( CPPDEFINES='with_'+self.name )
		if self.enabled(env,'incdir_'+self.name):
			#if self.language == 'c++':
			env.AppendUnique( CPPPATH=env['incdir_'+self.name] )
			if self.language == 'c':
				env.AppendUnique( CPATH=env['incdir_'+self.name] )

		if self.enabled(env,'libdir_'+self.name):
			env.AppendUnique( LIBPATH=env['libdir_'+self.name] )

		return True

	def postconfigure(self, project, env):
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
				conf.env.AppendUnique( LIBS = libname[:-1] )
				libname = libname[-1]
			return conf.CheckLibWithHeader( libname, header, language=language, call=call )
		else:
			conf.env.AppendUnique( LIBS = libname )
			#print 'no CheckLibWithHeader', self.name
			return True

	def CheckLib( self, conf, libname ):
		if conf.env['check_libs'] and not self.checkDone:
			if isinstance(libname, list) and len(libname) > 1:
				conf.env.AppendUnique( LIBS = libname[:-1] )
				libname = libname[-1]
			return conf.CheckLib( libname )
		else:
			conf.env.AppendUnique( LIBS = libname )
			#print 'no CheckLib', self.name
			return True

	def CheckHeader( self, conf, header, language ):
		if conf.env['check_libs'] and not self.checkDone:
			return conf.CheckHeader( header, language=language )
		else:
			#print 'no CheckHeader', self.name
			return True

