
from SCons.Environment import *
from SCons.Script import *

import sys
from time import *
import atexit
import os
import socket
import string
import subprocess
import getpass

import autoconf
import compiler
from utils import *
from utils.colors import *

class SConsProject:
	'''
	This is a base class helper for SCons build tool.
	In your SConstruct simply do:

	########################################
	# Example 1
	from sconsProject import SConsProject

	project = SConsProject()
	Export('project')
	Export({'libs':project.libs})

	project.begin()
	project.SConscript()
	project.end()

	########################################
	# Example 2
	# If you have common creation things in your project, create a class for your project which inherite this class.
	# So this function is accessible in all SConscript files.
	# You can also overload some SConsProject function to cusomize it.
	class MyProject( SConsProject ):

		def createCustomPlugins( self, sources=[], libs=[] ):
			"""
			Create a particular type of plugins from a sources list and a libraries list.
			"""
			pluginName = self.getName()
			env_local = self.createEnv( libs )
			env_local.AppendUnique( CCFLAGS = self.CC['visibilityhidden'] )
			plugin = env_local.SharedLibrary( target=pluginName, source=sources )
			env_local.InstallAs( self.inOutputBin(), plugin )

	project = MyProject()
	Export('project')
	Export({'libs':project.libs})

	project.begin()
	project.SConscript()
	project.end()
	########################################
	'''
	now               = strftime("%Y-%m-%d_%Hh%Mm%S", localtime())
	osname            = os.name.lower()
	sysplatform       = sys.platform.lower()
	hostname          = socket.gethostname()
	windows           = osname == "nt" and sysplatform.startswith("win")
	macos             = sysplatform.startswith("darwin")
	linux             = not windows and not macos
	unix              = not windows
	user              = getpass.getuser()

	compil_mode       = 'unknown_mode'
	dir               = os.getcwd()
	dir_output_build  = 'undefined'               #
	dir_output        = 'undefined'               #
	dir_output_bin    = 'undefined'               # name generated depending on compilation type,
	dir_output_lib    = 'undefined'               # we need to know if we are in debug mode, etc.
	dir_output_header = 'undefined'               # (options needs to be initilized)
	dir_output_test   = 'undefined'               #
	dir_sconsProject  = os.path.abspath(os.path.dirname(__file__)) # directory containing this file

	compiler          = ""
	libs              = autoconf
	commonLibs        = [libs.sconsProject]
	libs_help         = [] # temporary list of librairies already added to help
	libs_error        = [] # list of libraries with autoconf error
	allLibsChecked    = [] # temporary list of librairies already checked
	env               = Environment(tools=['default', 'packaging', 'doxygen', 'unittest',
									'qt4'], toolpath=[dir_sconsProject + "/tools"])

	def __init__(self):
		'''
		Initialisation of variables depending on computer.
		'''
		if self.windows:
			self.packagetype    = 'msi'
		else:
			self.packagetype    = 'rpm'

		if self.unix:
			if (os.uname()[4][-3:] == '_64'):
				self.bits = 64
			else:
				self.bits = 32
		elif self.windows:
			if 'PROGRAMFILES(X86)' not in os.environ:
				self.bits = 32
			else:
				self.bits = 64

		sconf = ['display',
		         'default',
		         'local' ]
		if self.unix:
			sconf.append( 'unix' )
			sconf.append( 'unix-'+str(self.bits) )
		if self.linux:
			sconf.append( 'linux' )
			sconf.append( 'linux-'+str(self.bits) )
		elif self.macos:
			sconf.append( 'macos' )
			sconf.append( 'macos-'+str(self.bits) )
		elif self.windows:
			sconf.append( 'windows' )
			sconf.append( 'windows-'+str(self.bits) )
		sconf.append( self.hostname )
		sconf.append( 'user' )
		sconf.append( self.user )
		sconf.append( 'finalize' )

		sconf_sconsProject = ['display', 'default']

		self.sconf_files = [
		                     os.path.join(self.dir_sconsProject, s)+'.sconf' for s in sconf_sconsProject
		                   ] + [
						     os.path.join(self.dir, s)+'.sconf' for s in sconf
						   ]
		self.sconf_files = [ f for f in self.sconf_files if os.path.exists(f) ]

		if self.windows:
			self.env['ENV']['PATH'] = os.environ['PATH'] # to have access to cl and link...

		# scons optimizations...
		self.env.SourceCode('.', None)
		self.env.Decider('MD5-timestamp')
		SetOption('implicit_cache', 1)
		SetOption('max_drift', 60 * 15) # cache the checksum after max_drift seconds


	#------------------------------------ Utils -----------------------------------#
	def printInfos(self):
		'''
		Print information at compilation's begining.
		'''
		sys.stdout.write(self.env['color_info'])
		print ':' * 80
		print '::' + ' '*32, self.env['mode'], 'mode'
		print ':' * 80
		print ':: dir                = ' + self.dir
		print ':: dir_output_build   = ' + self.dir_output_build
		print ':: dir_output_bin     = ' + self.dir_output_bin
		print ':: dir_output_lib     = ' + self.dir_output_lib
		print ':: dir_output_test    = ' + self.dir_output_test
		print ':: dir_sconsProject   = ' + self.dir_sconsProject
		print ':: now                = ' + self.now
		print ':: osname             = ' + self.osname
		print ':: sysplatform        = ' + self.sysplatform
		print ':: hostname           = ' + self.hostname
		print ':: compiler c         = ' + self.env['CC'] + (' (' + self.env['CCVERSION'] + ')' if 'CCVERSION' in self.env and self.env['CCVERSION'] else '')
		print ':: compiler c++       = ' + self.env['CXX'] + (' (' + self.env['CXXVERSION'] + ')' if 'CXXVERSION' in self.env and self.env['CXXVERSION'] else '')
		print ':: parallel jobs      = %d' % (GetOption('num_jobs'))
		if self.env['ccache']:
			print ':: ccachedir          = ' + self.env['ccachedir']
		print(':' * 80)
		sys.stdout.write(self.env['color_clear'])

	def printEnv(self, env=None, keys=[]):
		'''
		Debug function to display all environement options.
		'''
		if not env:
			print ':' * 20, ' env ', ':' * 20
			env = self.env
		if not keys:
			sys.stdout.write(self.env['color_info'])
			print env.Dump()
		else:
			print '*' * 50, 'keys: ', keys
			dict = env.Dictionary()
			for key in keys:
				if key in dict:
					sys.stdout.write(self.env['color_info'])
					print ':' * 10, ' %s = %s' % (key, dict[key])
		sys.stdout.write(self.env['color_clear'])

	def getRealAbsoluteCwd(self, relativePath=None):
		'''Returns original current directory (not inside the VariantDir)...'''
		dir = Dir('.').srcnode().abspath
		if isinstance(relativePath, list):
			return [self.getRealAbsoluteCwd(rp) for rp in relativePath]
		if relativePath:
			return os.path.join(dir, relativePath)
		else:
			return dir

	def getAbsoluteCwd(self, relativePath=None):
		'''Returns current directory...'''
		dir = Dir('.').abspath
		if relativePath:
			return os.path.join(dir, relativePath)
		else:
			return dir

	def getSubDirsAbsolutePath(self, current_dir=None):
		'''Returns sub-directories with absolute paths (in original file tree).'''
		if current_dir == None:
			current_dir = self.getRealAbsoluteCwd()
		else:
			current_dir = Dir('./' + current_dir).srcnode().abspath

		files = (os.listdir(current_dir)) # relative paths (only directories names)
		#files.append(current_dir)
		nonhidden = (f for f in files if f[0] != '.' and f.find('@'))
		absfiles = (os.path.join(current_dir, f) for f in nonhidden) # absolute paths
		dirs = (f for f in absfiles if os.path.isdir(f))
		return dirs

	def getSubDirs(self, current_dir=None):
		'''Returns sub-directories with relative paths (in original file tree).'''
		return map(os.path.basename, self.getSubDirsAbsolutePath(current_dir)) # absolute path -> relative path (for variant_dir)

	def getSubDirsWithSConscript(self):
		'''Returns sub-directories containing a SConscript file with relative paths (in original file tree).'''
		alldirs = self.getSubDirsAbsolutePath()
		dirs = (f for f in alldirs if os.path.isfile(os.path.join(f, 'SConscript')))
		ldirs = map(os.path.basename, dirs) # absolute path -> relative path (for variant_dir)
		return ldirs

	def inBuildDir(self, * dirs):
		'''Returns "dirs" as subdirectories of temporary "buildDir".'''
		if not dirs:
			return string.replace(os.getcwd(), self.dir, self.dir_output_build)
		return [string.replace(d, self.dir, self.dir_output_build) for d in dirs]

	def inTopDir(self, * dirs):
		'''Returns "dirs" as subdirectories of "topDir".'''
		basedir = self.dir + os.sep
		if not dirs:
			return basedir
		return [basedir + d for d in dirs]

	def inOutputDir(self, *dirs):
		'''Returns "dirs" as subdirectories of "outputDir".'''
		if not dirs:
			return self.dir_output
		return [ os.path.join( self.inOutputDir(), d ) for d in dirs ]

	def inOutputLib(self, *dirs):
		'''Returns "dirs" as subdirectories of "outputLib".'''
		if not dirs:
			return self.dir_output_lib
		return [ os.path.join( self.inOutputLib(), d ) for d in dirs ]

	def inOutputHeaders(self, *dirs):
		'''Returns "dirs" as subdirectories of "outputHeaders".'''
		if not dirs:
			return self.dir_output_header
		return [ os.path.join( self.inOutputHeaders(), d ) for d in dirs ]

	def inOutputBin(self, *dirs):
		'''Returns "dirs" as subdirectories of "outputBin".'''
		if not dirs:
			return self.dir_output_bin
		return [ os.path.join( self.inOutputBin(), d ) for d in dirs ]

	def inOutputTest(self, *dirs):
		'''Returns "dirs" as subdirectories of "outputTest".'''
		if not dirs:
			return self.dir_output_test
		return [ os.path.join( self.inOutputTest(), d ) for d in dirs ]

	def getName(self):
		'''Returns the current directory, often used as name.'''
		return os.path.basename(os.getcwd())

	def needConfigure(self):
		'''If the target builds nothing, we don't need to call the configure function.'''
		return not GetOption('clean') and not GetOption('help')

	def needCheck(self):
		'''If we check all libraries before compiling.'''
		return self.env['check_libs']

	#------------------------- Compilation options ----------------------------#
	def initOptions(self):
		'''
		Read options from configuration files and at last from the command line
		(which has the last word)
		'''
		if self.windows:
			self.compiler    = compiler.visual
		else:
			self.compiler    = compiler.gcc
		self.CC         = self.compiler.CC
		self.ccversion  = self.compiler.version(self.compiler.ccBin)
		self.cxxversion = self.compiler.version(self.compiler.cxxBin)

		# options from command line or configuration file
		self.opts = self.createOptions(self.sconf_files, ARGUMENTS)
		self.defineHiddenOptions(self.opts)
		self.opts_help = self.createOptions(self.sconf_files, ARGUMENTS)

		self.opts.Update(self.env)

		if 'icecc' in self.env['CC']:
			self.env['CCVERSION'] = self.compiler.version(self.env['ICECC_CC'])
			self.env['CXXVERSION'] = self.compiler.version(self.env['ICECC_CXX'])
			self.env['ENV']['ICECC_CC'] = self.env['ICECC_CC']
			self.env['ENV']['ICECC_CXX'] = self.env['ICECC_CXX']
		else:
			self.env['CCVERSION'] = self.compiler.version(self.env['CC'])
			self.env['CXXVERSION'] = self.compiler.version(self.env['CXX'])

	def createOptions(self, filename, args):
		'''
		Define options.
		'''
		opts = Variables(filename, args)

		def help_format(env, opt, help, default, actual, aliases):
			alignment = ' '*(len(opt)+2)
			multilineHelp = help.replace('\n', '\n'+alignment)
			return '%s%s%s  %s\n%s(default=%s, actual=%s)\n\n' % (self.env['color_title'], opt, self.env['color_clear'], multilineHelp, alignment, default, actual)
		opts.FormatVariableHelpText = help_format

		opts.Add(EnumVariable('mode', 'Compilation mode', 'debug', allowed_values=('debug', 'release', 'production')))
		opts.Add(BoolVariable('install', 'Install', False))
		opts.Add(BoolVariable('profile', 'Build with profiling support', False))
		opts.Add(BoolVariable('cover', 'Build with cover support', False))
		opts.Add(BoolVariable('clean', 'Remove all the build directory', False))
		opts.Add(BoolVariable('ignore_errors', 'Ignore any configuration errors', False))
#        opts.Add( BoolVariable( 'log',           'Enable output to a log file',                     False ) )
		opts.Add(BoolVariable('ccache', 'Enable compiler cache system (ccache style)', False))
		opts.Add(PathVariable('ccachedir', 'Cache directory', 'ccache', PathVariable.PathAccept))
		opts.Add(BoolVariable('colors', 'Using colors of the terminal', True if not self.windows else False))
		opts.Add('jobs', 'Parallel jobs', '1')
		opts.Add(BoolVariable('check_libs', 'Disable lib checking', True))
		opts.Add('CC', 'Specify the C Compiler', self.compiler.ccBin)
		opts.Add('CXX', 'Specify the C++ Compiler', self.compiler.cxxBin)

		opts.Add(PathVariable('ENVINC', 'Additional include path (at compilation)', '' if not self.windows else os.environ.get('INCLUDE', ''), PathVariable.PathAccept))
		opts.Add(PathVariable('ENVPATH', 'Additional bin path (at compilation)', '', PathVariable.PathAccept))
		opts.Add(PathVariable('ENVLIBPATH', 'Additional librairie path (at compilation)', '' if not self.windows else os.environ.get('LIB', ''), PathVariable.PathAccept))
		
		if self.windows:
			opts.Add(PathVariable('PROGRAMFILES', 'Program Files directory', os.environ.get('PROGRAMFILES', ''), PathVariable.PathAccept))
		
		opts.Add('CPPPATH', 'Additional preprocessor paths', [])
		opts.Add('CPPDEFINES', 'Additional preprocessor defines', [])
		opts.Add('LIBPATH', 'Additional library paths', [])
		opts.Add('LIBS', 'Additional libraries', [])
		# Don't explicitly put include directory arguments in CCFLAGS or CXXFLAGS
		# because the result will be non-portable and the directories will not
		# be searched by the dependency scanner.
		opts.Add('CCFLAGS', 'Additional C and C++ flags', [])
		opts.Add('CFLAGS', 'Additional C flags', [])
		opts.Add('CXXFLAGS', 'Additional C++ flags', [])
		opts.Add('LINKFLAGS', 'Additional linker flags', [])

		opts.Add('ICECC_CC', 'Compilator', self.compiler.ccBin)
		opts.Add('ICECC_CXX', 'Compilator', self.compiler.cxxBin)
		opts.Add('ICECC_VERSION', 'Compilator', '')

		buildDirName = '.dist' # base dir name for all intermediate compilation objects
		distDirName = 'dist'   # base dir name for output build
		opts.Add(PathVariable('BUILDPATH', 'Top directory of compilation tree', self.dir, PathVariable.PathIsDir))
		opts.Add('BUILDDIRNAME', 'Top directory of compilation tree', buildDirName)
		opts.Add(PathVariable('DISTPATH', 'Top directory to output compiled files', self.dir, PathVariable.PathIsDir))
		opts.Add('DISTDIRNAME', 'Directory name to output compiled files', distDirName)
		opts.Add(PathVariable('INSTALLPATH', 'Top directory to install compiled files', '${DISTPATH}/${DISTDIRNAME}', PathVariable.PathIsDirCreate))

		return opts

	def defineHiddenOptions(self, opts):
		'''
		Define basics options which don't need to be visible in the help.
		'''
		opts.Add(PathVariable('TOPDIR', 'Top directory', self.dir))

		opts.Add('osname', 'OS name', 'windows' if self.windows else 'unix')
		opts.Add('osbits', 'OS bits', self.bits)
		opts.Add(BoolVariable('unix', 'operating system', self.unix))
		opts.Add(BoolVariable('windows', 'operating system', self.windows))
		opts.Add(BoolVariable('macos', 'operating system', self.macos))
		opts.Add(BoolVariable('visualc', 'Compilator', self.windows))

		# display options
		opts.Add('SHCCCOMSTR', 'display option', '$SHCCCOM')
		opts.Add('SHCXXCOMSTR', 'display option', '$SHCXXCOM')
		opts.Add('SHLINKCOMSTR', 'display option', '$SHLINKCOM')
		opts.Add('CCCOMSTR', 'display option', '$CCCOM')
		opts.Add('CXXCOMSTR', 'display option', '$CXXCOM')
		opts.Add('LINKCOMSTR', 'display option', '$LINKCOM')
		opts.Add('ARCOMSTR', 'display option', '$ARCOM')
		opts.Add('INSTALLSTR', 'display option', 'Install file: $SOURCE as $TARGET')
		opts.Add('SWIG', 'swig binary', 'swig')
		opts.Add('SWIGCOMSTR', 'display option', '$SWIGCOM')
		opts.Add('QT_MOCFROMCXXCOMSTR', 'display option', '$QT_MOCFROMCXXCOM')
		opts.Add('QT_MOCFROMHCOMSTR', 'display option', '$QT_MOCFROMHCOM')
		opts.Add('QT_UICCOMSTR', 'display option', '$QT_UICCOM')

		opts.Add('color_clear', 'color', colors['clear'])
		opts.Add('color_red', 'color', colors['red'])
		opts.Add('color_redB', 'color', colors['redB'])
		opts.Add('color_green', 'color', colors['green'])
		opts.Add('color_blue', 'color', colors['blue'])
		opts.Add('color_blueB', 'color', colors['blueB'])
		opts.Add('color_yellow', 'color', colors['yellow'])
		opts.Add('color_brown', 'color', colors['brown'])
		opts.Add('color_violet', 'color', colors['violet'])

		opts.Add('color_autoconf', 'color', '')
		opts.Add('color_header', 'color', '')
		opts.Add('color_title', 'color', '')
		opts.Add('color_compile', 'color', '')
		opts.Add('color_link', 'color', '')
		opts.Add('color_install', 'color', '')

		opts.Add('color_info', 'color', '')
		opts.Add('color_success', 'color', '')
		opts.Add('color_warning', 'color', '')
		opts.Add('color_fail', 'color', '')
		opts.Add('color_error', 'color', colors['error'])


	def applyOptionsOnProject(self):
		'''
		Some options are used to modify the project (common to the whole compilation).
		'''
		subpath = os.path.join(self.hostname, '-'.join([self.compiler.name, self.env['CCVERSION']]), self.env['mode'])
		self.dir_output_build  = os.path.join(self.env['BUILDPATH'], self.env['BUILDDIRNAME'], subpath)
		install_dir = os.path.join(self.env['DISTPATH'], self.env['DISTDIRNAME'], subpath)
		if self.env['install']:
			install_dir = self.env['INSTALLPATH']
		self.dir_output        = install_dir
		self.dir_output_bin    = os.path.join(install_dir, 'bin')
		self.dir_output_lib    = os.path.join(install_dir, 'lib')
		self.dir_output_header = os.path.join(install_dir, 'include')
		self.dir_output_test   = os.path.join(install_dir, 'test')

		# temporary files of SCons inside the build directory
		self.env['CONFIGUREDIR'] = os.path.join(self.dir_output_build, 'sconf_temp')
		self.env['CONFIGURELOG'] = os.path.join(self.dir_output_build, 'config.log')
		SConsignFile(os.path.join(self.dir_output_build, 'sconsign.dblite'))

		if self.env['ccache']:
			if os.path.isabs(self.env['ccachedir']):
				CacheDir(self.env['ccachedir'])
			else:
				CacheDir(os.path.join(self.dir_output_build, self.env['ccachedir']))

		try:
			SetOption('num_jobs', int(self.env['jobs']))
		except:
			pass

		self.applyOptionsOnEnv(self.env)


	def applyOptionsOnEnv(self, env):
		'''
		Some options are used to modify others.
		'''

		env.PrependENVPath('INCLUDE', self.env['ENVINC'])
		env.PrependENVPath('PATH', self.env['ENVPATH'])
		env.PrependENVPath('LIB', self.env['ENVLIBPATH'])

		if not env['colors']:
			for c in ['color_clear', 'color_red', 'color_redB', 'color_green', 'color_blue', 'color_blueB', 'color_yellow', 'color_brown', 'color_violet', 'color_autoconf', 'color_header', 'color_title', 'color_compile', 'color_link', 'color_install', 'color_info', 'color_success', 'color_warning', 'color_fail', 'color_error']:
				env[c] = ''


	def SConscript(self, dirs=[], exports=[]):
		'''
		To include SConscript from SConstruct, this automatically define variantdirs.
		'''
		if not dirs:
			SConscript( self.inBuildDir(self.getAbsoluteCwd('SConscript')), exports=exports )
		else:
			for d in dirs:
				SConscript( dirs=self.inBuildDir(d), exports=exports )

	def begin(self):
		'''
		The begining function the SConstruct need to call at first of all.
		'''

		self.initOptions()
		self.applyOptionsOnProject()

		if self.env['clean']:
			Execute(Delete(self.dir_output_build))
			Exit(1)

		self.printInfos()

		VariantDir(self.dir_output_build, self.dir, duplicate=0)


	def end(self):
		'''
		The last function call at the end by the SConstruct.
		'''

		# by default compiles the target 'all'
		Default('all')

		doxygen = self.env.Doxygen(self.inTopDir('doc/config/Doxyfile'))

		self.env.Alias('doc', doxygen)
		self.env.Alias('doxygen', doxygen)
		self.env.Clean(doxygen, ['doc/html'])

		def printInstalledFiles(target, source, env):
			# Whatever it takes to build
			for t in FindInstalledFiles():
				print '*', t.name, ':'
				print ' '*5, t.abspath
			return None

		printInstalledFilesCmd = self.env.Command('always', '', printInstalledFiles)
		self.env.Alias('targets', printInstalledFilesCmd)

		if self.libs_error:
			sys.stdout.write(self.env['color_error'])
			for lib in self.libs_error:
				print "Error in '" + lib.name + "' library :"
				if lib.error:
					print '\t', lib.error
			sys.stdout.write(self.env['color_clear'])
			if not self.env['ignore_errors']:
				#raise 'BuildError', 'Configure errors... Compilation STOP !'
				print 'Configure errors... Compilation STOP !'
				print 'Use ignore_errors=1 to try to compile without correcting the problem.'
				Exit(1)
			sys.stdout.write(self.env['color_clear'])

		Help(
			 '''
		-- Usefull scons options --
			scons -Q               : making the SCons output less verbose
			scons -j               : parallel builds
			scons -i               : continue building after it encounters an error
			scons --tree           : display all or part of the SCons dependency graph
			scons --debug=presub   : pre-substitution string that SCons uses to generate the command lines it executes
			scons --debug=findlibs : display what library names SCons is searching for, and in which directories it is searching

	'''
			 )

		Help(
			 '''
		-- Build options --
			scons                  : build all plugins and programs
			scons plugins          : build all plugins
			scons pluginName       : build the plugin named 'pluginName'
			scons doc              : build doxygen documentation

	'''
			 )

		Help(self.opts_help.GenerateHelpText(self.env))

		# register function to display compilation status at the end
		# to avoid going through if SCons raises an exception (error in a SConscript)
		atexit.register(utils.display_build_status)


#-------------------------------- Autoconf ------------------------------------#

	def createEnv(self, libs=[], name=''):
		'''
		Create an environment from the common one and apply libraries configuration to this environment.
		@todo : add opts=[] ?
		'''
		new_env = self.env.Clone()
		new_libs = list(libs)
		for lib in self.commonLibs:
			new_libs.insert(0, lib) # prepend (self.libs.sconsProject)

		return self.appendLibsToEnv( new_env, new_libs, name )

	def appendLibsToEnv(self, env, libs=[], name=''):
		'''
		Append libraries to an environment.
		'''
		if not libs:
			return env

		sys.stdout.write(self.env['color_autoconf']) # print without new line

		if 'SconsProjectLibraries' in env:
			env['SconsProjectLibraries'] += libs
		else:
			env['SconsProjectLibraries'] = libs

		opts_current = self.createOptions(self.sconf_files, ARGUMENTS)
		self.defineHiddenOptions(opts_current)
		
		allLibs = []
		for eachlib in libs:
			libdeps = self.findLibsDependencies(eachlib)
			allLibs.extend( libdeps )
			allLibs.append( eachlib )
		allLibs = self.uniqLibs(allLibs)

		#print 'libs:', [a.name for a in libs]
		#print 'allLibs:', [a.name for a in allLibs]
		#print '-'*10
		
		for lib in allLibs:
			if not lib.initOptions(self, opts_current):
				if lib not in self.libs_error:
					self.libs_error.append(lib)
			if lib not in self.libs_help:
				lib.initOptions(self, self.opts_help)
				self.libs_help.append(lib)
		opts_current.Update(env)
		self.applyOptionsOnEnv(env)

		if self.needConfigure():
			for lib in allLibs:
				if not lib.enabled(env):
					print 'Target "'+name+'" compiled without "'+lib.name+'" library.'
				else:
					self.checkLibrary( lib )

					if not lib.configure(self, env):
						if lib not in self.libs_error:
							self.libs_error.append(lib)
					else:
						conf = env.Configure()
						if not lib.check(self, conf):
							if lib not in self.libs_error:
								self.libs_error.append(lib)
						env = conf.Finish()

		for lib in allLibs:
			lib.postconfigure(self, env)

		sys.stdout.write(self.env['color_clear'])

		return env

	def checkLibrary( self, lib=None ):
		'''
		Create a temporary environment, apply all library dependencies and do
		a check on lib.
		'''
		if lib.checkDone:
			return

		# if it's an internal library, no check
		if lib.sconsNode:
			return
		
		if lib.name in self.allLibsChecked:
			#print 'Already checked ', lib.name
			lib.checkDone = True
			return
		
		#print '_'*20
		#print 'checkLibrary: ', lib.name

		if not self.needCheck():
			lib.checkDone = True
			self.allLibsChecked.append( lib.name )
			return

		dependencies = self.uniqLibs( self.findLibsDependencies(lib) )

		#print "_"*50
		#print "lib.name:", lib.name
		#print "dependencies:", [d.name for d in dependencies]

		check_env = self.env.Clone()

		check_opts = self.createOptions(self.sconf_files, ARGUMENTS)
		self.defineHiddenOptions(check_opts)
		for a in dependencies:
			a.initOptions(self, check_opts)
		if not lib.initOptions(self, check_opts):
			if lib not in self.libs_error:
				self.libs_error.append(lib)
		check_opts.Update(check_env)
		self.applyOptionsOnEnv(check_env)

		for a in dependencies:
			a.configure(self, check_env)
		if not lib.configure(self, check_env):
			if lib not in self.libs_error:
				self.libs_error.append(lib)
		check_conf = check_env.Configure()
		for a in dependencies:
			a.check(self, check_conf)
		if not lib.check(self, check_conf):
			if lib not in self.libs_error:
				self.libs_error.append(lib)
		check_env = check_conf.Finish()

		lib.checkDone = True
		self.allLibsChecked.append( lib.name )

	def uniqLibs(self, allLibs):
		'''
		Return the list of libraries contains in allLibs without any duplication.
		'''
		libs = []
		names = []
		for s in allLibs:
			if s.name not in names:
				names.append( s.name )
				libs.append( s )
		return libs

	def findLibsDependencies(self, libs):
		'''
		return the list of all dependencies of lib (without the lib itself).
		'''
		def internFindLibDependencies(lib):
			if not lib:
				return []
			ll = []
			for l in lib.dependencies:
				ll.extend( internFindLibDependencies(l) )
			ll.append(lib)
			return ll
		
		if not isinstance(libs, list):
			libs = [libs]
		ll = []
		for lib in libs:
			for l in lib.dependencies:
				ll.extend( internFindLibDependencies(l) )
		return ll

# todo
#    def Install(self):
#        
#        env.AddPostAction(obj , Chmod(str(obj),bin_mode) )

#-------------------------------- Autoconf ------------------------------------#
	def appendDict( self, dst, src ):
		'''
		Append the src dict into dst.
		If elements are not a list type, put it into a list to merge the values.
		'''
		for k, v in src.items():
			if k in dst:
				if isinstance(dst[k], list):
					dst[k] += v if isinstance(v, list) else [v]
				else:
					dst[k] = dst[k] + (v if isinstance(v, list) else [v])
			else:
				dst[k] = v

	def ObjectLibrary( self, name, libraries=[], includes=[], envFlags={} ):
		'''
		To create an ObjectLibrary and expose it in the project to be easily used by other targets.
		This is not a library just a configuration object with CPPDEFINES, CCFLAGS, LIBS, etc.
		'''
		# expose this library
		dstLibChecker = autoconf._internal.InternalLibChecker( name=name, includes=includes, envFlags=envFlags, dependencies=libraries )

		# add the new declared library to the list of libs checker in self.libs
		setattr(self.libs, name, dstLibChecker)

		return dstLibChecker

	def StaticLibrary( self, target, sources=[], dirs=[], env=None, libraries=[], includes=[], localEnvFlags={}, replaceLocalEnvFlags={},
	                         externEnvFlags={}, globalEnvFlags={}, dependencies=[], installDir=None, install=True,
	                         accept=['*.cpp', '*.cc', '*.c'], reject=['@', '_qrc', '_ui', '.moc.cpp'], shared=False ):
		'''
		To create a StaticLibrary and expose it in the project to be simply used by other targets.
		The shared option allows to create a static library compiled with position independant code (like in shared libraries).
		'''
		sourcesFiles = []
		sourcesFiles += sources
		if dirs:
			sourcesFiles += self.scanFiles( dirs, accept, reject )

		if not sourcesFiles:
			raise LogicError( "No source files for the target: " + target )

		localEnv = None
		if env:
			localEnv = env
			self.appendLibsToEnv(localEnv, libraries)
		else:
			# if no environment we create a new one
			localEnv = self.createEnv( libraries, name=target )

		# apply arguments to env
		localEnv.AppendUnique( CPPPATH = self.getRealAbsoluteCwd(dirs+includes) )
		if localEnvFlags:
			localEnv.AppendUnique( **localEnvFlags )
		if replaceLocalEnvFlags:
			localEnv.Replace( **replaceLocalEnvFlags )
		if globalEnvFlags:
			localEnv.AppendUnique( **globalEnvFlags )

		if shared:
			localEnv.AppendUnique( CCFLAGS = self.CC['sharedobject'] )
			localEnv['OBJSUFFIX'] = '.os'
			localEnv.AppendUnique( CCFLAGS = localEnv['SHCCFLAGS'] )
			localEnv.AppendUnique( LINKFLAGS = localEnv['SHLINKFLAGS'] )

		# create the target
		dstLib = localEnv.StaticLibrary( target=target, source=sourcesFiles )

		# explicitly create dependencies to all internal libraries used
		# i.e. internal libraries need to be compiled before this target
		internalLibsDepends = [ l.sconsNode for l in libraries if l.sconsNode ] # if there is a sconsNode inside the library it's an internal lib
		if internalLibsDepends:
			localEnv.Depends( dstLib, internalLibsDepends )
		
		dstLibInstall = localEnv.Install( installDir if installDir else self.inOutputLib(), dstLib ) if install else dstLib
		localEnv.Alias( target, dstLibInstall )

		# expose this library
		envFlags=externEnvFlags
		self.appendDict( envFlags, globalEnvFlags )
		dstLibChecker = autoconf._internal.InternalLibChecker( lib=target, includes=self.getRealAbsoluteCwd(includes), envFlags=envFlags, dependencies=libraries+dependencies, sconsNode=dstLibInstall )

		# add the new declared library to the list of libs checker in self.libs
		setattr(self.libs, target, dstLibChecker)

		return dstLibInstall

	def SharedLibrary( self, target, sources=[], dirs=[], env=None, libraries=[], includes=[], localEnvFlags={}, replaceLocalEnvFlags={},
	                         externEnvFlags={}, globalEnvFlags={}, dependencies=[], installDir=None, install=True,
	                         accept=['*.cpp', '*.cc', '*.c'], reject=['@', '_qrc', '_ui', '.moc.cpp'] ):
		'''
		To create a SharedLibrary and expose it in the project to be simply used by other targets.
		'''
		sourcesFiles = []
		sourcesFiles += sources
		if dirs:
			sourcesFiles += self.scanFiles( dirs, accept, reject )

		if not sourcesFiles:
			raise LogicError( "No source files for the target: " + target )
		
		localEnv = None
		localLibraries = libraries
		if env:
			localEnv = env
			self.appendLibsToEnv(localEnv, localLibraries)
			if 'SconsProjectLibraries' in localEnv:
				localLibraries += localEnv['SconsProjectLibraries']
		else:
			# if no environment we create a new one
			localEnv = self.createEnv( localLibraries, name=target )

		# apply arguments to env
		localEnv.AppendUnique( CPPPATH = self.getRealAbsoluteCwd(dirs+includes) )
		if localEnvFlags:
			localEnv.AppendUnique( **localEnvFlags )
		if replaceLocalEnvFlags:
			localEnv.Replace( **replaceLocalEnvFlags )
		if globalEnvFlags:
			localEnv.AppendUnique( **globalEnvFlags )

		# create the target
		dstLib = localEnv.SharedLibrary( target=target, source=sourcesFiles )

		# explicitly create dependencies to all internal libraries used
		# i.e. internal libraries need to be compiled before this target
		internalLibsDepends = [ l.sconsNode for l in localLibraries if l.sconsNode ] # if there is a sconsNode inside the library it's an internal lib
		if internalLibsDepends:
			localEnv.Depends( dstLib, internalLibsDepends )

		dstLibInstall = localEnv.Install( installDir if installDir else self.inOutputLib(), dstLib ) if install else dstLib
		localEnv.Alias( target, dstLibInstall )

		# expose this library
		envFlags=externEnvFlags
		self.appendDict( envFlags, globalEnvFlags )
		dstLibChecker = autoconf._internal.InternalLibChecker( lib=target, includes=self.getRealAbsoluteCwd(includes), envFlags=envFlags, dependencies=localLibraries+dependencies, sconsNode=dstLibInstall )

		# add the new declared library to the list of libs checker in self.libs
		setattr(self.libs, target, dstLibChecker)

		return dstLibInstall


#-------------------- Automatic file/directory search -------------------------#
	def asList(self, v):
		'''Return v inside a list if not a list.'''
		if isinstance(v, list):
			return v
		return [v]

	def recursiveDirs(self, root):
		'''List of subdirectories.'''
		if sys.version_info < (2, 6):
			return filter((lambda a: a.rfind("CVS") == -1), [a[0] for a in os.walk(root)])
		else:
			return filter((lambda a: a.rfind("CVS") == -1), [a[0] for a in os.walk(root, followlinks=True)])

	def unique(self, seq):
		'''Removes duplicates. Element order preserved.'''
		seen = set()
		return [x for x in seq if x not in seen and not seen.add(x)]

	def scanFilesInDir(self, directory, accept, reject):
		'''
		Recursively search files in "directory" that matches 'accepts' wildcards and don't contains "reject"
		'''
		l_accept = self.asList( accept )
		l_reject = self.asList( reject )
		sources = []
		realcwd = self.getRealAbsoluteCwd()
		paths = self.recursiveDirs( self.getRealAbsoluteCwd(directory) )
		for path in paths:
			for pattern in l_accept:
				sources += Glob(os.path.join(path, pattern), strings=True) # string=True to return files as strings
		for pattern in l_reject:
			sources = filter((lambda a: a.rfind(pattern) == -1), sources)
		# to relative paths (to allow scons variant_dir to recognize files...)
		def toLocalDirs(d): return d.replace(realcwd + os.sep, '')
		lsources = map(toLocalDirs, sources)
		return self.unique(lsources)

	def scanFiles(self, dirs=['.'], accept=['*.cpp', '*.cc', '*.c'], reject=['@', '_qrc', '_ui', '.moc.cpp']):
		'''
		Recursively search files in "dirs" that matches 'accepts' wildcards and don't contains "reject"
		'''
		l_dirs = self.asList( dirs )
		files = []
		for d in l_dirs:
			files += self.scanFilesInDir(d, accept, reject)
		return files

	def dirnames(self, files):
		'''Returns the list of files dirname.'''
		dirs = self.unique(map(os.path.dirname, files))
		dirs.sort()
		return dirs

	def subdirsContaining(self, dir, patterns):
		'''
		Returns all sub directories of 'dir' containing a file matching 'patterns'.
		'''
		dirs = self.dirnames(self.scanFiles(dir, accept=patterns))
		dirs.sort()
		return dirs


__all__ = ['SConsProject']

