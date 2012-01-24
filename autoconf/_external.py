from _base import *

class LibWithHeaderChecker(BaseLibChecker):

	def __init__(self, libs, header, language, name=None, call=None, dependencies=[], version='', defines=[], flags=[], cppflags=[], linkflags=[] ):
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
		self.dependencies = asList(dependencies)
		self.version = str(version)
		self.defines = asList(defines)
		self.flags = asList(flags)
		self.cppflags = asList(cppflags)
		self.linkflags = asList(linkflags)

	def initOptions(self, project, opts):
		BaseLibChecker.initOptions(self, project, opts)
		opts.Add( 'incdir_'+self.name, 'Include directories for '+self.name, '${_join_if_basedir_not_empty( dir_'+self.name+ ', "include" )}' )
		opts.Add( 'libdir_'+self.name, 'Link directories for '+self.name, '${_join_if_basedir_not_empty( dir_'+self.name+ ', "lib" )}' )
		return True

	def check(self, project, conf):
		result = self.CheckLibWithHeader( conf, self.getLibs(conf.env), self.header, self.language, call=self.call )
		return result


class LibChecker(BaseLibChecker):

	def __init__(self, libs, name=None, dependencies=[], version='', defines=[], flags=[], cppflags=[], linkflags=[] ):
		if not name:
			if isinstance(libs, list):
				self.name = libs[0]
			else:
				self.name = libs
		else:
			self.name = name
		self.libs = asList(libs)
		self.dependencies = asList(dependencies)
		self.version = str(version)
		self.defines = asList(defines)
		self.flags = asList(flags)
		self.cppflags = asList(cppflags)
		self.linkflags = asList(linkflags)

	def initOptions(self, project, opts):
		BaseLibChecker.initOptions(self, project, opts)
		opts.Add( 'incdir_'+self.name, 'Include directory for '+self.name, '${_join_if_basedir_not_empty( dir_'+self.name+ ', "include" )}' )
		opts.Add( 'libdir_'+self.name, 'Link directories for '+self.name, '${_join_if_basedir_not_empty( dir_'+self.name+ ', "lib" )}' )
		return True

	def check(self, project, conf):
		result = self.CheckLib( conf, self.getLibs(conf.env) )
		return result


class HeaderChecker(BaseLibChecker):

	def __init__( self, name, header, language, dependencies=[], version='', libs=[], defines=[], flags=[], cppflags=[], linkflags=[] ):
		self.name = name
		self.header   = header
		self.language = language
		self.dependencies = asList(dependencies)
		self.version = str(version)
		self.defines = asList(defines)
		self.flags = asList(flags)
		self.cppflags = asList(cppflags)
		self.linkflags = asList(linkflags)

	def initOptions(self, project, opts):
		BaseLibChecker.initOptions(self, project, opts)
		opts.Add( 'incdir_'+self.name, 'Include directory for '+self.name, '${_join_if_basedir_not_empty( dir_'+self.name+ ', "include" )}' )
		opts.Add( 'libdir_'+self.name, 'Link directories for '+self.name, '${_join_if_basedir_not_empty( dir_'+self.name+ ', "lib" )}' )
		return True

	def postconfigure(self, project, env, level):
		'''
		Particular case, which allow to add things after all libraries checks.
		'''
		env.AppendUnique( LIBS = self.getLibs(env) )
		return True

	def check(self, project, conf):
		result = self.CheckHeader( conf, self.header, language=self.language )
		return result

class ObjectChecker(BaseLibChecker):

	def __init__( self, name, dependencies=[], version='', defines=[], flags=[], cppflags=[], linkflags=[] ):
		self.name = name
		self.dependencies = asList(dependencies)
		self.version = str(version)
		self.defines = asList(defines)
		self.flags = asList(flags)
		self.cppflags = asList(cppflags)
		self.linkflags = asList(linkflags)

	def initOptions(self, project, opts):
		BaseLibChecker.initOption_with(self, project, opts)
		return True

	def check(self, project, conf):
		return True


