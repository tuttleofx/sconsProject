from _external import *
import os

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

	def __init__( self,
				  modules = [
					  'QtCore',
					  'QtGui',
					  'QtOpenGL',
#				'QtAssistant',
#				'QtScript',
#				'QtDBus',
#				'QtSql',
#				'QtNetwork',
#				'QtSvg',
#				'QtTest',
#				'QtXml',
#				'QtUiTools',
#				'QtDesigner',
#				'QtDesignerComponents',
#				'QtWebKit'
#				'Qt3Support',
				],
				  uiFiles = [],
				  defines = ['QT_NO_KEYWORDS'],
				  useLocalIncludes = True ):
		self.name  = 'qt4'
		self.libs = modules
		self.uiFiles = uiFiles
		self.defines = defines
		self.useLocalIncludes = useLocalIncludes
		
	def setModules(self, modules):
		self.libs = modules
		
	def declareUiFiles(self, uiFiles):
		self.uiFiles = uiFiles

	def initOptions(self, project, opts):
		LibWithHeaderChecker.initOptions(self, project, opts)
		opts.Add( 'bindir_'+self.name,   'Base directory for '+self.name, os.path.join('$dir_'+self.name, 'bin') )
		return True

	def configure(self, project, env):
		env.EnableQtEmmitters()

		bindir = '$bindir_'+self.name
		moc = locateQt4Command(env, 'moc', bindir)
		uic = locateQt4Command(env, 'uic', bindir)
		rcc = locateQt4Command(env, 'rcc', bindir)
		lupdate = locateQt4Command(env, 'lupdate', bindir)
		lrelease = locateQt4Command(env, 'lrelease', bindir)
		#print 'moc', moc
		env.SetDefault(
				QT_MOC = moc,
				QT_UIC = uic,
				QT4_RCC = rcc,
				QT4_LUPDATE = lupdate,
				QT4_LRELEASE = lrelease,
			)
		
		return BaseLibChecker.configure(self, project, env)
	
	def check(self, project, conf):
		conf.env.AppendUnique( CPPDEFINES = self.defines )
		result = True
		for mod in self.libs:
			r = self.CheckLibWithHeader( conf, [mod], header=[mod+'/'+mod], language='c++' )
			if not r:
				print 'error: ',mod
			result &= r
		return result
	
	def postconfigure(self, project, env):
		'''
		Cas particulier. Permet d'ajouter des elements a l'environnement apres les checks de toutes les libs.
		'''
		if len(self.uiFiles):
			uis = [env.Uic( ui ) for ui in self.uiFiles]
			if self.useLocalIncludes:
				env.AppendUnique( CPPPATH=subdirs(self.uiFiles) )
		return True

qt4 = Qt4Checker


