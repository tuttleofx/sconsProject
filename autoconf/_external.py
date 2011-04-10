from _base import *

class LibWithHeaderChecker(BaseLibChecker):

	def __init__(self, libs, header, language, name=None, call=None, dependencies=[], defines=[] ):
		self.libs = asList(libs)
		#print 'name:', name
		#print 'libs:', self.libs
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
		self.dependencies = list(dependencies)
		self.defines = list(defines)

	def initOptions(self, project, opts):
		BaseLibChecker.initOptions(self, project, opts)
		opts.Add( 'incdir_'+self.name, 'Include directories for '+self.name, os.path.join('$dir_'+self.name, 'include') )
		opts.Add( 'libdir_'+self.name, 'Link directories for '+self.name, os.path.join('$dir_'+self.name, 'lib') )
		return True

	def check(self, project, conf):
		conf.env.AppendUnique( CPPDEFINES = self.defines )
		result = self.CheckLibWithHeader( conf, self.getLibs(conf.env), self.header, self.language, call=self.call )
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
		self.libs = asList(libs)
		self.dependencies = dependencies
		self.defines = defines

	def initOptions(self, project, opts):
		BaseLibChecker.initOptions(self, project, opts)
		opts.Add( 'incdir_'+self.name, 'Include directory for '+self.name, os.path.join('$dir_'+self.name, 'include') )
		opts.Add( 'libdir_'+self.name, 'Link directories for '+self.name, os.path.join('$dir_'+self.name, 'lib') )
		return True

	def check(self, project, conf):
		conf.env.AppendUnique( CPPDEFINES = self.defines )
		result = self.CheckLib( conf, self.getLibs(conf.env) )
		return result


class HeaderChecker(BaseLibChecker):

	def __init__(self, name, header, language, dependencies=[], libs=[], defines=[]):
		self.name = name
		self.header   = header
		self.language = language
		self.dependencies = dependencies
		self.defines = defines
		self.libs = asList(libs)

	def initOptions(self, project, opts):
		BaseLibChecker.initOptions(self, project, opts)
		opts.Add( 'incdir_'+self.name, 'Include directory for '+self.name, os.path.join('$dir_'+self.name, 'include') )
		opts.Add( 'libdir_'+self.name, 'Link directories for '+self.name, os.path.join('$dir_'+self.name, 'lib') )
		return True

	def postconfigure(self, project, env):
		'''
		Particular case, which allow to add things after all libraries checks.
		'''
		env.AppendUnique( LIBS = self.getLibs(env) )
		return True

	def check(self, project, conf):
		conf.env.AppendUnique( CPPDEFINES = self.defines )
		result = self.CheckHeader( conf, self.header, language=self.language )
		return result
