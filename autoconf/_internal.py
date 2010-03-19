
from SCons import Variables
from SCons import Environment

from _base import *

class InternalLibChecker(BaseLibChecker):

	def __init__(self, lib='', name='', includes=[], envFlags={}, dependencies=[] ):
		self.lib  = lib
		if name:
			self.name = name
		else:
			self.name = lib
		self.includes= includes
		self.envFlags = envFlags
		self.dependencies = dependencies

	def enabled(self,env,option=None):
		'''Can't disable an internal library.'''
		return True

	def initOptions(self, putois, opts):
		'''No options for internal library.'''
		return True
	
	def configure(self, putois, env):
		'''
		Add things to the environment.
		'''
		if self.includes:
			env.AppendUnique( CPPPATH = self.includes )
		
		if self.envFlags:
			env.AppendUnique( **(self.envFlags) )

		# we don't set LIBPATH because it's setted by the project

		return True

	def postconfigure(self, putois, env):
		'''Don't check for local lib, so we only add it.'''
		if self.lib:
			env.AppendUnique( LIBS = self.lib )

