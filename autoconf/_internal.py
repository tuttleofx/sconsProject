
from SCons import Variables
from SCons import Environment

from _base import *

class InternalLibChecker(BaseLibChecker):

	def __init__(self, lib='', name='', includes=[], envFlags={}, dependencies=[], sconsNode=None ):
		self.lib  = lib # the target (name of the library file without prefix or extension)
		if name:
			self.name = name
		else:
			self.name = lib
		self.includes= includes # includes directories
		self.envFlags = envFlags # library specific flags
		self.dependencies = dependencies # all libraries needed by this library (need to be propagated to all targets using this library)
		self.sconsNode = sconsNode # a reference to the scons node object, we can use to use Depends, Alias, etc.

	def enabled(self,env,option=None):
		'''Can't disable an internal library.'''
		return True

	def initOptions(self, project, opts):
		'''No options for internal library.'''
		return True
	
	def configure(self, project, env):
		'''
		Add things to the environment.
		'''
		if self.includes:
			env.AppendUnique( CPPPATH = self.includes )
		
		if self.envFlags:
			env.AppendUnique( **(self.envFlags) )

		# we don't set LIBPATH because it's setted by the project

		return True

	def postconfigure(self, project, env):
		'''Don't check for local lib, so we only add it.'''
		if self.lib:
			env.AppendUnique( LIBS = self.lib )

