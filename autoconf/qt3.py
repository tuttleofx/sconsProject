from _external import *
import os

def unique(list):
	return dict.fromkeys(list).keys()

def subdirs(files):
	dirs = unique(map(os.path.dirname, files))
	dirs.sort()
	return dirs

def locateQt3Command(env, command, bindir):
	#print 'locateQt3Command:', command
	suffixes = [
		'-qt3',
		'3',
		'',
	]
	progs = [command+s for s in suffixes]
	for prog in progs:
		path = env.WhereIs(prog, path=bindir)
		if path:
			return path
	
	msg = 'Qt3 command "' + command + '" not found. Tried: ' + str(progs) + '.'
	#raise Exception(msg)
	print 'Warning: ', msg
	return command

class Qt3Checker(LibWithHeaderChecker):
	'''
	Qt3 checker
	'''

	def __init__( self,
				  modules = [
					  'qt',
					  'qui',
				],
				  uiFiles = [],
				  defines = ['QT_NO_KEYWORDS'],
				  useLocalIncludes = True ):
		self.name  = 'qt3'
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
		moc = locateQt3Command(env, 'moc', bindir)
		uic = locateQt3Command(env, 'uic', bindir)
		rcc = locateQt3Command(env, 'rcc', bindir)
		lupdate = locateQt3Command(env, 'lupdate', bindir)
		lrelease = locateQt3Command(env, 'lrelease', bindir)
		#print 'moc', moc
		env.SetDefault(
				QT_MOC = moc,
				QT_UIC = uic,
				QT_RCC = rcc,
				QT_LUPDATE = lupdate,
				QT_LRELEASE = lrelease,
			)
		# depends the developper syntax used
		# maybe we need to expose these values as parameters (in initOptions)
		env.Replace(
				QT_UICDECLPREFIX = '', # this is the standard value for qt3
				QT_UICDECLSUFFIX = '.h',
			)
		
		return BaseLibChecker.configure(self, project, env)
	
	def check(self, project, conf):
		conf.env.AppendUnique( CPPDEFINES = self.defines )
		result = self.CheckLibWithHeader( conf, self.libs, header=['qapplication.h'], language='c++' )
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

qt3 = Qt3Checker


