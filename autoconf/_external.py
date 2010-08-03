from _base import *

class LibWithHeaderChecker(BaseLibChecker):

	def __init__(self, libs, header, language, name=None, call=None, dependencies=[], defines=[] ):
		self.libname  = libs
		self.header   = header
		self.language = language
		self.call = call
		if not name:
			if isinstance(libs, list):
				self.name = libs[0]
			else:
				self.name = libs
		else:
			self.name = name
		self.dependencies = dependencies
		self.defines = defines

	def initOptions(self, project, opts):
		BaseLibChecker.initOptions(self, project, opts)
		opts.Add( 'incdir_'+self.name, 'Include directories for '+self.name,  None )
		opts.Add( 'libdir_'+self.name, 'Link directories for '+self.name,     None )
		return True

	def check(self, project, conf):
		conf.env.AppendUnique( CPPDEFINES = self.defines )
		result = self.CheckLibWithHeader( conf, self.libname, self.header, self.language, call=self.call )
		self.checkDone = True
		#print 'checkDone LibWithHeaderChecker: ', result
		return result


class LibChecker(BaseLibChecker):

	def __init__(self, libs, name=None, dependencies=[], defines=[] ):
		if not name:
			if isinstance(libs, list):
				self.name = libs[0]
			else:
				self.name = libs
		else:
			self.name = name
		self.libname = libs
		self.dependencies = dependencies
		self.defines = defines

	def initOptions(self, project, opts):
		BaseLibChecker.initOptions(self, project, opts)
		opts.Add( 'libdir_'+self.name, 'Link directories for '+self.name, None )
		opts.Add( 'incdir_'+self.name, 'Include directory for '+self.name, None )
		return True

	def check(self, project, conf):
		conf.env.AppendUnique( CPPDEFINES = self.defines )
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

	def initOptions(self, project, opts):
		BaseLibChecker.initOptions(self, project, opts)
		opts.Add( 'incdir_'+self.name, 'Include directory for '+self.name, None )
		opts.Add( 'libdir_'+self.name, 'Link directories for '+self.name, None )
		return True

	def postconfigure(self, project, env):
		'''
		Particular case, which allow to add things after all libraries checks.
		'''
		env.AppendUnique( LIBS = self.libs )
		return True

	def check(self, project, conf):
		conf.env.AppendUnique( CPPDEFINES = self.defines )
		result = self.CheckHeader( conf, self.header, language=self.language )
		self.checkDone = True
		#print 'checkDone HeaderChecker: ', result
		return result


class FrameworkChecker(BaseLibChecker):

	def __init__(self, frameworks, header, language, name=None, call=None, dependencies=[], defines=[] ):
		if not macos:
			raise LogicError( 'Frameworks exists only on MacOS.' )
		if not name:
			if isinstance(frameworks, list):
				self.name = frameworks[0]
			else:
				self.name = frameworks
		else:
			self.name = name
		self.header   = header
		self.language = language
		self.frameworks = frameworks
		self.call     = call
		self.defines  = defines
		self.dependencies = dependencies
		self.libs = []

	def initOptions(self, project, opts):
		BaseLibChecker.initOptions(self, project, opts)
		opts.Add( 'fwdir_'+self.name, 'Framework directory for '+self.name,     None )
		return True

	def check(self, project, conf):
		conf.env.AppendUnique( CPPDEFINES = self.defines )
		result = self.CheckFrameworkWithHeader( conf, self.frameworks, self.header, self.language, call=self.call )
		self.checkDone = True
		#print 'checkDone LibWithHeaderChecker: ', result
		return result

