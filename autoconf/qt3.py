from _external import *
from SCons.Script import *
from glew import *
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
	#print 'Warning: ', msg
	return command

class Qt3Checker(LibWithHeaderChecker):
	'''
	Qt3 checker
	'''
	allUiFiles = []

	def __init__( self,
				  modules = [
					  'qt-mt',
					  'qui',
				],
				  uiFiles = [],
				  defines = ['QT_NO_KEYWORDS','QT_THREAD_SUPPORT'],
				  useLocalIncludes = True ):
		self.name  = 'qt3'
		self.libs = modules[:]
		self.uiFiles = self.getAbsoluteCwd(uiFiles)
		self.defines = defines[:]
		self.dependencies = [glew]
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
		result = self.CheckLibWithHeader( conf, self.getLibs(conf.env), header=['qapplication.h'], language='c++' )
		return result
	
	def postconfigure(self, project, env, level):
		'''
		Add things for ui files after all libs check.
		'''
		if len(self.uiFiles):
			for ui in self.uiFiles:
				# do not redeclare a ui file
				if ui not in Qt3Checker.allUiFiles:
					env.Uic( ui )
					Qt3Checker.allUiFiles.append( ui )
			if self.useLocalIncludes:
				env.AppendUnique( CPPPATH=subdirs(self.uiFiles) )
		return True

qt3 = Qt3Checker


