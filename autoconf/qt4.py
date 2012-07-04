from _external import *
import os
import SCons.Util

def unique(list):
	return dict.fromkeys(list).keys()

def subdirs(files):
	dirs = unique(map(os.path.dirname, files))
	dirs.sort()
	return dirs

def locateQt4Command(env, command, bindir):
	#print 'locateQt4Command:', command
	suffixes = [
		'-qt4',
		'4',
		'',
	]
	progs = [command+s for s in suffixes]
	for prog in progs:
		path = env.WhereIs(prog, path=bindir)
		if path:
			return path
	for prog in progs:
		path = env.WhereIs(prog)
		if path:
			return path
	
	msg = 'Qt4 command "' + command + '" not found. Tried: ' + str(progs) + '.'
	#raise Exception(msg)
	print 'Warning: ', msg
	return command

class Qt4Checker(LibWithHeaderChecker):
	'''
	Qt4 checker
	'''
	allUiFiles = []

	def __init__( self,
				  modules = [
					  'QtCore',
					  'QtGui',
					  'QtOpenGL',
#					'QtAssistant',
#					'QtScript',
#					'QtDBus',
#					'QtSql',
#					'QtNetwork',
#					'QtSvg',
#					'QtTest',
#					'QtXml',
#					'QtUiTools',
#					'QtDesigner',
#					'QtDesignerComponents',
#					'QtWebKit'
#					'Qt3Support',
					],
				  uiFiles = [],
				  defines = ['QT_NO_KEYWORDS'],
				  useLocalIncludes = True ):
		self.name  = 'qt4'
		postfix = '' if not windows else '4'
		self.libs = [ m + postfix for m in modules]
		self.uiFiles =self.getAbsoluteCwd(uiFiles)
		self.defines = defines[:]
		self.useLocalIncludes = useLocalIncludes
		
	def setModules(self, modules):
		self.libs = modules[:]
		
	def declareUiFiles(self, uiFiles):
		self.uiFiles.extend( self.getAbsoluteCwd(uiFiles) )

	def initEnv(self, project, env):
		# use qt scons tool
		env.Tool('qt')

	def initOptions(self, project, opts):
		LibWithHeaderChecker.initOptions(self, project, opts)
		opts.Add( 'bindir_'+self.name,   'Base directory for '+self.name, '${_join_if_basedir_not_empty( dir_'+self.name+ ', "bin" )}' )
		return True

	def configure(self, project, env):
		env.EnableQtEmmitters()

		bindir = '$bindir_'+self.name
		moc = locateQt4Command(env, 'moc', bindir)
		uic = locateQt4Command(env, 'uic', bindir)
		rcc = locateQt4Command(env, 'rcc', bindir)
		lupdate = locateQt4Command(env, 'lupdate', bindir)
		lrelease = locateQt4Command(env, 'lrelease', bindir)
		
		# specific part for Qt4
		env.Replace(
				# suffixes/prefixes for the headers / sources to generate
				QT_UICDECLPREFIX = 'ui_',
				QT_UICDECLSUFFIX = '.h',
				QT_UICIMPLPREFIX = 'ui_',
				QT_UICIMPLSUFFIX = '$CXXFILESUFFIX',
				QT_MOCHPREFIX = 'moc_',
				QT_MOCHSUFFIX = '$CXXFILESUFFIX',
				QT_MOCCXXPREFIX = '',
				QT_MOCCXXSUFFIX = '.moc',
				QT_UISUFFIX = '.ui',

				# Qt commands
				# command to generate header from a .ui file
				QT_UICCOM = [
				    SCons.Util.CLVar('$QT_UIC $QT_UICDECLFLAGS -o ${TARGETS[0]} $SOURCE'),
				],
			)
		
		env.SetDefault(
				QT_MOC = moc,
				QT_UIC = uic,
				QT4_RCC = rcc,
				QT4_LUPDATE = lupdate,
				QT4_LRELEASE = lrelease,
			)
		
		# don't need emitter with qt4
		env['BUILDERS']['Uic'].emitter = None
		
		return BaseLibChecker.configure(self, project, env)
	
	def check(self, project, conf):
		conf.env.AppendUnique( CPPDEFINES = self.defines )
		result = True
		for mod in self.getLibs(conf.env):
			r = self.CheckLibWithHeader( conf, [mod], header=[mod+'/'+mod], language='c++' )
			if not r:
				print 'error: ',mod
			result &= r
		return result
	
	def postconfigure(self, project, env, level):
		'''
		Add things for ui files after all libs check.
		'''
		if len(self.uiFiles):
			for ui in self.uiFiles:
				# do not redeclare a ui file
				if ui not in Qt4Checker.allUiFiles:
					env.Uic( ui )
					Qt4Checker.allUiFiles.append( ui )
			if self.useLocalIncludes:
				env.AppendUnique( CPPPATH=subdirs(self.uiFiles) )
		return True

qt4 = Qt4Checker


