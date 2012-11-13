"""SConsProject

The SConsProject module proposes a way to easily create the compilation system
of your project with the minimum of information. It's an helper around SCons.

"""

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

def join_if_basedir_not_empty( *dirs ):
	'''
	Join directories like standard 'os.path.join' function but with the particular case that if the first directory is empty, the function return an empty string.
	For example if you join '' and 'include', the result is ''.
	'''
	if not dirs or not dirs[0]:
		return ''
	return os.path.join(*dirs)


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

	project = MyProject(
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

	modes = ('debug', 'release', 'production')
	compil_mode       = 'unknown_mode'
	dir               = os.getcwd()
	dir_output_build  = 'undefined'               #
	dir_output        = 'undefined'               #
	dir_output_bin    = 'undefined'               # name generated depending on compilation type,
	dir_output_lib    = 'undefined'               # we need to know if we are in debug mode, etc.
	dir_output_plugin = 'undefined'
	dir_output_header = 'undefined'               # (options needs to be initilized)
	dir_output_test   = 'undefined'               #
	dir_sconsProject  = os.path.abspath(os.path.dirname(__file__)) # directory containing this file

	compiler          = None
	libs              = autoconf
	commonLibs        = [libs.sconsProject]
	libs_help         = [] # temporary list of librairies already added to help
	libs_error        = [] # list of libraries with autoconf error
	allLibsChecked    = [] # temporary list of librairies already checked
	env               = Environment( tools=[
                                            'packaging',
                                            'doxygen',
                                            'unittest',
                                            'scripttest',
                                            ] + (['msvs'] if windows else []),
                                         toolpath=[os.path.join(dir_sconsProject,'tools')] )
	
	allVisualProjects = []

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

		sconf = [
			'display',
			'default',
			'local',
			'host',
			]
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

		#if self.windows:
		self.env['ENV']['PATH'] = os.environ['PATH'] # access to the compiler (if not in '/usr/bin')

		# scons optimizations...
		# http://www.scons.org/wiki/GoFastButton
		#
		# Next line is important, it deactivates tools search for default variable, just note that now in SConscript you have 
		# to use env.Program(...) instead of simply Program().
		SCons.Defaults.DefaultEnvironment(tools = [])
		# Avoid RCS and SCCS scans by using env.SourceCode(".", None) - this is especially interesting if you are using lots of c or c++ headers in your program and that your file system is remote (nfs, samba).
		self.env.SourceCode('.', None)
		# as of SCons 0.98, you can set the Decider function on an environment. MD5-timestamp says if the timestamp matches, don't bother re-MD5ing the file. This can give huge speedups.
		self.env.Decider('MD5-timestamp')
		# This option tells SCons to intelligently cache implicit dependencies. It attempts to determine if the implicit dependencies have changed since the last build, and if so it will recalculate them. This is usually slower than using --implicit-deps-unchanged, but is also more accurate.
		SetOption('implicit_cache', 1)
		# By default SCons will calculate the MD5 checksum of every source file in your build each time it is run, and will only cache the checksum after the file is 2 days old. This default of 2 days is to protect from clock skew from NFS or revision control systems. You can tweak this delay using --max-drift=SECONDS where SECONDS is some number of seconds. Decreasing SECONDS can improve build speed by eliminating superfluous MD5 checksum calculations.
		SetOption('max_drift', 60 * 15) # cache the checksum after max_drift seconds
		# Normally you tell Scons about include directories by setting the CPPPATH construction variable, which causes SCons to search those directories when doing implicit dependency scans and also includes those directories in the compile command line. If you have header files that never or rarely change (e.g. system headers, or C run-time headers), then you can exclude them from CPPPATH and include them in the CCFLAGS construction variable instead, which causes SCons to ignore those include directories when scanning for implicit dependencies. Carefully tuning the include directories in this way can usually result in a dramatic speed increase with very little loss of accuracy.
		# To achieve this we add a new variable 'EXTERNCPPPATH' which is the same as CPPPATH but without searching for implicit dependencies in those directories. So we always use EXTERNCPPPATH for external libraries.
		self.env['_CPPINCFLAGS'] = '$( ${_concat(INCPREFIX, CPPPATH,       INCSUFFIX, __env__, RDirs, TARGET, SOURCE)} ' \
		                           '${_concat(INCPREFIX, EXTERNCPPPATH, INCSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)'
		self.env['_join_if_basedir_not_empty'] = join_if_basedir_not_empty


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
		print ':: dir_output_plugin  = ' + self.dir_output_plugin
		print ':: dir_output_lib     = ' + self.dir_output_lib
		print ':: dir_output_test    = ' + self.dir_output_test
		print ':: dir_sconsProject   = ' + self.dir_sconsProject
		print ':: now                = ' + self.now
		print ':: osname             = ' + self.osname
		print ':: sysplatform        = ' + self.sysplatform
		print ':: hostname           = ' + self.hostname
		ccversion = str(self.env['CCVERSION']) if 'CCVERSION' in self.env and self.env['CCVERSION'] else ''
		print ':: compiler c         = ' + str(self.env['CC']) + ' (' + ccversion + ')'
		cxxversion = str(self.env['CXXVERSION']) if ('CXXVERSION' in self.env) and (self.env['CXXVERSION']) else ''
		print ':: compiler c++       = ' + str(self.env['CXX']) + ' (' + cxxversion + ')'
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

	def getAllAbsoluteCwd(self, relativePath=None):
		'''
		Returns current directory (in original path and VariantDir path) or relativePath in current directory.
		Paths are absolute.
		Returns a list.
		'''
		if isinstance(relativePath, list):
			alldirs = []
			for rp in relativePath:
				alldirs.extend( self.getAllAbsoluteCwd(rp) )
			return alldirs
		if relativePath:
			if relativePath.startswith('#'):
				return [os.path.join(self.dir, relativePath[1:]),
				        os.path.join(self.dir_output_build, relativePath[1:])]
			elif os.path.isabs(relativePath):
				if relativePath.startswith(self.dir_output_build):
					return [relativePath,
					        os.path.join(self.dir, relativePath[len(self.dir_output_build)+1:])]
				elif relativePath.startswith(self.dir):
					return [relativePath,
					        os.path.join(self.dir_output_build, relativePath[len(self.dir)+1:])]
				else:
					return [relativePath]
			else:
				return [os.path.join(Dir('.').srcnode().abspath, relativePath),
				        os.path.join(Dir('.').abspath, relativePath)]
		else:
			return [Dir('.').srcnode().abspath,
			        Dir('.').abspath]

	def getRealAbsoluteCwd(self, relativePath=None):
		'''
		Returns original current directory (not inside the VariantDir) or relativePath in original current directory.
		Paths are absolute.
		'''
		if isinstance(relativePath, list):
			return [self.getRealAbsoluteCwd(rp) for rp in relativePath]
		cdir = Dir('.').srcnode().abspath
		if relativePath:
			if isinstance(relativePath, SCons.Node.FS.Dir):
				return relativePath.srcnode().abspath
			elif relativePath.startswith('#'):
				return os.path.join(self.dir, relativePath[1:])
			elif os.path.isabs(relativePath):
				return relativePath
			return os.path.join(cdir, relativePath)
		else:
			return cdir

	def getAbsoluteCwd(self, relativePath=None):
		'''
		Returns current directory or relativePath in current directory.
		Paths are absolute.
		'''
		if isinstance(relativePath, list):
			return [self.getAbsoluteCwd(rp) for rp in relativePath]
		cdir = Dir('.').abspath
		if relativePath:
			if relativePath.startswith('#'):
				return os.path.join(self.dir_output_build, relativePath[1:])
			elif os.path.isabs(relativePath):
				return relativePath
			return os.path.join(cdir, relativePath)
		else:
			return cdir

	def getCwdInProject(self):
		cdir = Dir('.').srcnode().abspath
		return os.path.relpath(cdir, self.dir)

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
			return string.replace(os.getcwd(), self.dir, self.dir_output_build, 1)
		if len(dirs) == 1 and isinstance(dirs[0], str):
			d = dirs[0]
			if not d.startswith(self.dir_output_build):
				return string.replace(d, self.dir, self.dir_output_build, 1)
			else:
				return d
		l_dirs = SCons.Util.flatten(dirs)
		return [ self.inBuildDir(d) for d in l_dirs ]

	def inTopDir(self, * dirs):
		'''Returns "dirs" as subdirectories of "topDir".'''
		if not dirs:
			return self.dir
		if len(dirs) == 1:
			if issubclass(dirs[0].__class__, SCons.Node.FS.Base):
				return dirs[0]
			elif isinstance(dirs[0], str):
				if os.path.isabs( dirs[0] ):
					return dirs[0]
				return os.path.join(self.inTopDir(), dirs[0])
		l_dirs = SCons.Util.flatten(dirs)
		return [ self.inTopDir(d) for d in l_dirs ]

	def inOutputDir(self, *dirs):
		'''Returns "dirs" as subdirectories of "outputDir".'''
		if not dirs:
			return self.dir_output
		if len(dirs) == 1 and isinstance(dirs[0], str):
			return os.path.join( self.inOutputDir(), dirs[0] )
		l_dirs = SCons.Util.flatten(dirs)
		return [ self.inOutputDir(d) for d in l_dirs ]

	def inOutputLib(self, *dirs):
		'''Returns "dirs" as subdirectories of "outputLib".'''
		if not dirs:
			return self.dir_output_lib
		if len(dirs) == 1 and isinstance(dirs[0], str):
			return os.path.join( self.inOutputLib(), dirs[0] )
		l_dirs = SCons.Util.flatten(dirs)
		return [ self.inOutputLib(d) for d in l_dirs ]

	def inOutputHeaders(self, *dirs):
		'''Returns "dirs" as subdirectories of "outputHeaders".'''
		if not dirs:
			return self.dir_output_header
		if len(dirs) == 1 and isinstance(dirs[0], str):
			return os.path.join( self.inOutputHeaders(), dirs[0] )
		l_dirs = SCons.Util.flatten(dirs)
		return [ self.inOutputHeaders(d) for d in l_dirs ]

	def inOutputBin(self, *dirs):
		'''Returns "dirs" as subdirectories of "outputBin".'''
		if not dirs:
			return self.dir_output_bin
		if len(dirs) == 1 and isinstance(dirs[0], str):
			return os.path.join( self.inOutputBin(), dirs[0] )
		l_dirs = SCons.Util.flatten(dirs)
		return [ self.inOutputBin(d) for d in l_dirs ]

	def inOutputPlugin(self, *dirs):
		'''Returns "dirs" as subdirectories of "outputPlugin".'''
		if not dirs:
			return self.dir_output_plugin
		if len(dirs) == 1 and isinstance(dirs[0], str):
			return os.path.join( self.inOutputPlugin(), dirs[0] )
		l_dirs = SCons.Util.flatten(dirs)
		return [ self.inOutputPlugin(d) for d in l_dirs ]

	def inOutputTest(self, *dirs):
		'''Returns "dirs" as subdirectories of "outputTest".'''
		if not dirs:
			return self.dir_output_test
		if len(dirs) == 1 and isinstance(dirs[0], str):
			return os.path.join( self.inOutputTest(), dirs[0] )
		l_dirs = SCons.Util.flatten(dirs)
		return [ self.inOutputTest(d) for d in l_dirs ]

	def getName(self, n=1):
		'''Create a name using the current directory. "n" is the number of parents to build the name.'''
		v = self.getCwdInProject().split(os.sep)
		if n == 0:
			return '_'.join( v )
		return '_'.join( v[-n:] )

	def getDirs(self, n=1):
		'''Create a list of upper directories. "n" is the number of parents.'''
		alldirs = self.getCwdInProject().split(os.sep)
		if isinstance( n, list ):
			return [alldirs[i] for i in n]
		else:
			return alldirs[-n:]

        def convertSconsPathToStr(self, *dirs):
                '''Returns "dirs" as str.'''
                if len(dirs) == 1:
                        if issubclass(dirs[0].__class__, SCons.Node.FS.Base):
                                return dirs[0].srcnode().abspath
                        elif isinstance(dirs[0], str):
                                return dirs[0]
                l_dirs = SCons.Util.flatten(dirs)
                return [ self.convertSconsPathToStr(d) for d in l_dirs ]

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

		self.env.Tool('default')
		# default values
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

		# select the environment from user options
		compilerName = self.env['compiler']
		self.compiler   = eval( 'compiler.' + compilerName )
		self.CC         = self.compiler.CC

		if self.windows:
			if compilerName == 'visual':
				self.env.Tool('default')
				self.env.Tool('msvc')
			elif compilerName == 'gcc':
				self.env.Tool('mingw')
			else:
				self.env.Tool('default')
				print 'Error: Unrecognized compiler value on this platform. ('+str(compilerName)+')'

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

		opts.Add(EnumVariable('mode', 'Compilation mode', 'production', allowed_values=self.modes))
		opts.Add(BoolVariable('install', 'Install', False))
		opts.Add(BoolVariable('profile', 'Build with profiling support', False))
		opts.Add(BoolVariable('cover', 'Build with cover support', False))
		opts.Add(BoolVariable('clean', 'Remove all the build directory', False))
		opts.Add(BoolVariable('ignore_errors', 'Ignore any configuration errors', False))
#        opts.Add( BoolVariable( 'log',           'Enable output to a log file',                     False ) )
		opts.Add(BoolVariable('ccache', 'Enable compiler cache system (ccache style)', False))
		opts.Add(PathVariable('ccachedir', 'Cache directory', 'ccache', PathVariable.PathAccept))
		opts.Add(BoolVariable('colors', 'Using colors of the terminal', True if not self.windows else False))
		opts.Add('default', 'Default objects to build', 'all')
		opts.Add('aliases', 'A list of custom aliases.', [])
		opts.Add('jobs', 'Parallel jobs', '1')
		opts.Add(BoolVariable('check_libs', 'Disable lib checking', True))
		opts.Add('CC', 'Specify the C Compiler', self.compiler.ccBin)
		opts.Add('CXX', 'Specify the C++ Compiler', self.compiler.cxxBin)

		opts.Add('SCRIPTTESTXX', 'Specify the script test binary', "nosetests")
		opts.Add('SCRIPTTESTFLAGS', 'Specify the script test flags', "")

		opts.Add('ENVINC', 'Additional include path (at compilation)', [] if not self.windows else os.environ.get('INCLUDE', '').split(':'))
		opts.Add('ENVPATH', 'Additional bin path (at compilation)', [])
		opts.Add('ENVLIBPATH', 'Additional librairie path (at compilation)', [] if not self.windows else os.environ.get('LIB', '').split(':'))
		
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
		opts.Add(BoolVariable('linux', 'operating system', self.linux))
		opts.Add(BoolVariable('windows', 'operating system', self.windows))
		opts.Add(BoolVariable('macos', 'operating system', self.macos))
		opts.Add('compiler', 'Choose compiler mode. This defines all flag system to use.', 'visual' if self.windows else 'gcc')

		opts.Add('EXTERNCPPPATH', 'Additional preprocessor paths (like CPPPATH but without dependencies check)', [])

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
		self.bits = int(self.env['osbits'])
		self.dir_output_build  = os.path.join(self.env['BUILDPATH'], self.env['BUILDDIRNAME'], subpath)
		install_dir = os.path.join(self.env['DISTPATH'], self.env['DISTDIRNAME'], subpath)
		if self.env['install']:
			install_dir = self.env['INSTALLPATH']
		self.dir_output        = install_dir
		self.dir_output_bin    = os.path.join(install_dir, 'bin')
		self.dir_output_lib    = os.path.join(install_dir, 'lib')
		self.dir_output_plugin = os.path.join(install_dir, 'plugin')
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
		To include SConscript from SConstruct, this automatically defines variantdirs.
		'''
		if not dirs:
			sconscriptFilename = self.inBuildDir(self.getAbsoluteCwd('SConscript'))
			SConscript( sconscriptFilename, exports=exports )
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
		if self.windows:
			visualSolution = self.env.MSVSSolution(
				target = 'project' + self.env['MSVSSOLUTIONSUFFIX'],
				projects = self.allVisualProjects,
				variant = [m.capitalize() for m in self.modes], )
			self.env.Depends( visualSolution, self.allVisualProjects )
			self.env.Alias( 'visualSolution', visualSolution )

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
				print ''' '''
				print '''Configure errors... Can't start compilation!'''
				print '''See config.log to check the problem details.'''
				print ''' '''
				print '''Use ignore_errors=1 to try to compile without fixing the problem. Maybe you can build a subpart of the project.'''
				print ''' '''
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

		# user can add some aliases
		for v in self.env['aliases']:
			self.env.Alias(v[0], v[1:])

		# by default compiles the target 'all'
		if isinstance(self.env['default'], str):
			Default( self.env['default'].split() )
		else:
			Default( self.env['default'] )
		
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
			allLibs.append( (eachlib,0) )
		allLibs = self.uniqLibs(allLibs)

		#print 'libs:', [a.name for a in libs]
		#print 'allLibs:', [a.name for a in allLibs]
		#print '-'*10
		
		for lib, level in allLibs:
			if not lib.initOptions(self, opts_current):
				if lib not in self.libs_error:
					self.libs_error.append(lib)
			if lib not in self.libs_help:
				lib.initOptions(self, self.opts_help)
				self.libs_help.append(lib)
		opts_current.Update(env)
		self.applyOptionsOnEnv(env)

		for lib, level in allLibs:
			lib.initEnv(self, env)

		if self.needConfigure():
			for lib, level in allLibs:
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

		for lib, level in allLibs:
			lib.postconfigure(self, env, level)

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
		for a, level in dependencies:
			a.initOptions(self, check_opts)
		if not lib.initOptions(self, check_opts):
			if lib not in self.libs_error:
				self.libs_error.append(lib)
		check_opts.Update(check_env)
		self.applyOptionsOnEnv(check_env)

		for a, level in dependencies:
			a.initEnv(self, check_env)
		lib.initEnv(self, check_env)
		for a, level in dependencies:
			a.configure(self, check_env)
		if not lib.configure(self, check_env):
			if lib not in self.libs_error:
				self.libs_error.append(lib)
		check_conf = check_env.Configure()
		for a, level in dependencies:
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
		for s, level in allLibs:
			if (s.name, s.id) not in names:
				names.append( (s.name, s.id) )
				libs.append( (s,level) )
		return libs

	def findLibsDependencies(self, libs):
		'''
		return the list of all dependencies of lib (without the lib itself).
		'''
		def internFindLibDependencies(lib, level=0):
			if not lib:
				return []
			ll = []
			for l in lib.dependencies:
				ll.extend( internFindLibDependencies(l, level+1) )
			ll.append( (lib,level) )
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
				vlist = (v if isinstance(v, list) else [v])
				if isinstance(dst[k], list):
					dst[k].extend( vlist )
				else:
					dst[k] = [dst[k]] + vlist
			else:
				dst[k] = v

	def prepareIncludes(self, dirs):
		objDirs = [Dir(d) for d in self.getAllAbsoluteCwd(dirs)]
		objDirs = self.unique(objDirs)
		return objDirs

	def MSVSProject(self, targetName, buildTarget,
			sources=[], headers=[], localHeaders=[],
			resources=[], misc=[],
			env=None
			):
		if not self.windows:
			return

		l_env = env.Clone() if env else self.env.Clone()
		l_buildTarget = self.asList( buildTarget )
		#print 'visualProject...'
		mode = l_env['mode'].capitalize()

		#visualProjectFile = os.path.join('visualc', targetName + envLocal['MSVSPROJECTSUFFIX'])
		visualProjectFile = targetName + l_env['MSVSPROJECTSUFFIX']
		#print '_-'*40
		#print 'targetName:', targetName
		##print 'visualProjectFile:', visualProjectFile
		##print 'target:', self.getRealAbsoluteCwd(visualProjectFile)
		##print '[buildTarget[0]]:', [buildTarget[0]]

		#print 'srcs:', [os.path.normpath( self.getRealAbsoluteCwd(i) ) for i in sources]
		#print '-'*20
		#print 'incs:', [os.path.normpath( self.getRealAbsoluteCwd(i) ) for i in headers]
		#print '-'*20
		##print 'localincs:', localIncludes
		#print 'local abs incs:', [os.path.normpath( self.getRealAbsoluteCwd(i) ) for i in localHeaders]
		#print '-'*20
		
		# add EXTERNCPPPATH to the standard CPPPATH, to add those include paths to the visualProject
		l_env.AppendUnique( CPPPATH = l_env['EXTERNCPPPATH'] )
		l_env.Replace( CPPPATH = self.convertSconsPathToStr(l_env['CPPPATH']) )

		visualProject = l_env.MSVSProject(
			target = os.path.normpath( self.getRealAbsoluteCwd(visualProjectFile) ),
			srcs = [ os.path.normpath( self.getRealAbsoluteCwd(i) ) for i in sources],
			incs = [ os.path.normpath( self.getRealAbsoluteCwd(i) ) for i in headers],
			localincs = [ os.path.normpath( self.getRealAbsoluteCwd(i) ) for i in localHeaders],
			resources = resources,
			misc = misc,
			buildtarget = buildTarget[0],
			auto_build_solution = False,
			variant = self.env['mode'].capitalize() #[m.capitalize() for m in self.modes],
			)
		self.allVisualProjects.append( visualProject )
		self.env.Alias( 'visualProject-'+targetName, visualProject )

	def ObjectLibrary( self, target,
			libraries=[], includes=[], envFlags={}, sources=[],
			public=True, publicName=None,
			):
		'''
		To create an ObjectLibrary and expose it in the project to be easily used by other targets.
		This is not a library just a configuration object with CPPDEFINES, CCFLAGS, LIBS, etc.
		'''
		l_libraries = self.asList(libraries)
		l_includes = self.asList(includes)
		l_sources = self.asList(sources)
		unusedLocalEnv = self.createEnv( l_libraries, name=target )
		# expose this library
		dstLibChecker = autoconf._internal.InternalLibChecker( name=target, includes=self.prepareIncludes(l_includes), envFlags=envFlags, dependencies=l_libraries, addSources=self.getRealAbsoluteCwd(l_sources) )

		# add the new declared library to the list of libs checker in self.libs
		if public:
			if publicName:
				setattr(self.libs, publicName, dstLibChecker)
			else:
				setattr(self.libs, target, dstLibChecker)

		return dstLibChecker

	def StaticLibrary( self, target,
			sources=[], precsrc='', precinc='', dirs=[], libraries=[], includes=[],
			env=None, localEnvFlags={}, replaceLocalEnvFlags={}, externEnvFlags={}, globalEnvFlags={},
			dependencies=[], installDir=None, installAs=None, install=True,
			headers=[], localHeaders=[],
			accept=['*.cpp', '*.cc', '*.c'], reject=['@', '_qrc', '_ui', '.moc.cpp'],
			shared=False, public=True, publicName=None,
			):

		'''
		To create a StaticLibrary and expose it in the project to be simply used by other targets.
		The shared option allows to create a static library compiled with position independant code (like in shared libraries).
		
		target: name of the target file
		sources: list of source files
		dirs: list of directories that contains the sources files
		libraries: list of libraries
		includes: list of include directories
		env: you can specify your custom environment to create the library
		localEnvFlags: defines some flags locally
		replaceLocalEnvFlags: defines some flags locally
		externEnvFlags: defines some flags for external usage of the library (only other targets that use the current library will have these flags)
		globalEnvFlags: defines some flags
		dependencies: 
		installDir: Destination directory to install the target
		installAs: Full path of the fil to install
		install: install the target (in the default or custom dir or renamed using installAs)
		headers: headers to include in the project (not for build, but project generation eg. visualProject)
		localHeaders: headers to include in the project (not for build, but project generation eg. visualProject)
		accept: pattern to filter the source files search in @p dirs
		reject: pattern to filter the source files search in @p dirs
		public: If you declares the library as public, it can be used by other targets.
		'''
		l_sources = self.asList(sources)
		l_dirs = self.asList(dirs)
		l_libraries = self.asList(libraries)
		l_includes = self.asList(includes)
		sourcesFiles = []
		sourcesFiles += l_sources
		if l_dirs:
			sourcesFiles += self.scanFiles( l_dirs, accept, reject, inBuildDir=True )

		if not sourcesFiles:
			raise RuntimeError( "No source files for the target: " + target )

		localEnv = None
		if env:
			localEnv = env.Clone()
			self.appendLibsToEnv(localEnv, l_libraries)
		else:
			# if no environment we create a new one
			localEnv = self.createEnv( libraries, name=target )

		# apply arguments to env
		localIncludes = self.prepareIncludes(l_dirs+l_includes)
		localEnv.AppendUnique( CPPPATH = localIncludes )
		if localEnvFlags:
			localEnv.AppendUnique( **localEnvFlags )
		if replaceLocalEnvFlags:
			localEnv.Replace( **replaceLocalEnvFlags )
		if globalEnvFlags:
			localEnv.AppendUnique( **globalEnvFlags )

		if shared:
			localEnv.AppendUnique( CCFLAGS = self.CC['sharedobject'] )
			localEnv['OBJSUFFIX'] = '.os'
			if 'SHCCFLAGS' in localEnv:
				localEnv.AppendUnique( CCFLAGS = localEnv['SHCCFLAGS'] )
			if 'SHLINKFLAGS' in localEnv:
				localEnv.AppendUnique( LINKFLAGS = localEnv['SHLINKFLAGS'] )
		
		if 'ADDSRC' in localEnv:
			sourcesFiles = sourcesFiles + localEnv['ADDSRC']
		
		sourcesFiles = self.getAbsoluteCwd( sourcesFiles )

		#adding precompiled headers
		if precinc and self.windows:
			localEnv['PCHSTOP'] = self.getRealAbsoluteCwd() + '/' + precinc
			localEnv.Append( CPPFLAGS = [ '/FI' + self.getRealAbsoluteCwd() + '/' + precinc, '/Zm135' ] )
			localEnv['PCH'] = localEnv.PCH( precsrc )[0]

		# create the target
		dstLib = localEnv.StaticLibrary( target=target, source=sourcesFiles )

		# explicitly create dependencies to all internal libraries used
		# i.e. internal libraries need to be compiled before this target
		internalLibsDepends = [ l.sconsNode for l in libraries if l.sconsNode ] # if there is a sconsNode inside the library it's an internal lib
		if internalLibsDepends:
			localEnv.Depends( dstLib, internalLibsDepends )
		
		dstLibInstall = dstLib
		if install:
			if installDir:
				dstLibInstall = localEnv.Install( installDir, dstLib )
			elif installAs:
				dstLibInstall = localEnv.InstallAs( installAs, dstLib[0] )
			else:
				dstLibInstall = localEnv.Install( self.inOutputLib(), dstLib )

		localEnv.Alias( target, dstLibInstall )
		localEnv.Alias( 'all', target )

		if self.windows:
			l_headers = self.scanFiles( l_dirs, accept=['*.h', '*.hpp', '*.tcc', '*.inl', '*.H'] ) + headers
			self.MSVSProject( target, dstLibInstall,
				sources=sourcesFiles,
				headers=l_headers, localHeaders=localHeaders,
				env = localEnv,
				)

		# expose this library
		envFlags=externEnvFlags
		self.appendDict( envFlags, globalEnvFlags )
		dstLibChecker = autoconf._internal.InternalLibChecker( lib=target, includes=self.prepareIncludes(l_includes), envFlags=envFlags, dependencies=libraries+dependencies, sconsNode=dstLibInstall )

		# add the new declared library to the list of libs checker in self.libs
		if public:
			if publicName:
				setattr(self.libs, publicName, dstLibChecker)
			else:
				setattr(self.libs, target, dstLibChecker)

		return dstLibInstall

	def SharedLibrary( self, target,
				sources=[], precsrc='', precinc='', dirs=[], libraries=[], includes=[],
				env=None, localEnvFlags={}, replaceLocalEnvFlags={}, externEnvFlags={}, globalEnvFlags={},
				dependencies=[], installDir=None, installAs=None, install=True,
				headers=[], localHeaders=[],
				accept=['*.cpp', '*.cc', '*.c'], reject=['@', '_qrc', '_ui', '.moc.cpp'],
				public=True, publicName=None,
			):
		'''
		To create a SharedLibrary and expose it in the project to be simply used by other targets.

		target: name of the target file
		sources: list of source files
		dirs: list of directories that contains the sources files
		libraries: list of libraries
		includes: list of include directories
		env: you can specify your custom environment to create the library
		localEnvFlags: defines some flags locally
		replaceLocalEnvFlags: defines some flags locally
		externEnvFlags: defines some flags for external usage of the library (only other targets that use the current library will have these flags)
		globalEnvFlags: defines some flags
		dependencies: 
		installDir: Destination directory to install the target
		installAs: Full path of the fil to install
		install: install the target (in the default or custom dir or renamed using installAs)
		headers: headers to include in the project (not for build, but project generation eg. visualProject)
		localHeaders: headers to include in the project (not for build, but project generation eg. visualProject)
		accept: pattern to filter the source files search in @p dirs
		reject: pattern to filter the source files search in @p dirs
		public: If you declares the library as public, it can be used by other targets.
		'''
		l_sources = self.asList(sources)
		l_dirs = self.asList(dirs)
		l_libraries = self.asList(libraries)
		l_includes = self.asList(includes)
		sourcesFiles = []
		sourcesFiles += l_sources
		if l_dirs:
			sourcesFiles += self.scanFiles( l_dirs, accept, reject, inBuildDir=True )

		if not sourcesFiles:
			raise RuntimeError( "No source files for the target: " + target )
		
		localEnv = None
		localLibraries = l_libraries
		if env:
			localEnv = env.Clone()
			self.appendLibsToEnv(localEnv, localLibraries)
			if 'SconsProjectLibraries' in localEnv:
				localLibraries += localEnv['SconsProjectLibraries']
		else:
			# if no environment we create a new one
			localEnv = self.createEnv( localLibraries, name=target )

		# apply arguments to env
		localIncludes = self.prepareIncludes(l_dirs+l_includes)
		localEnv.AppendUnique( CPPPATH = localIncludes )
		if localEnvFlags:
			localEnv.AppendUnique( **localEnvFlags )
		if replaceLocalEnvFlags:
			localEnv.Replace( **replaceLocalEnvFlags )
		if globalEnvFlags:
			localEnv.AppendUnique( **globalEnvFlags )

		if 'ADDSRC' in localEnv:
			sourcesFiles = sourcesFiles + localEnv['ADDSRC']

		sourcesFiles = self.getAbsoluteCwd( sourcesFiles )
		
		#adding precompiled headers
		if precinc and self.windows:
			localEnv['PCHSTOP'] = self.getRealAbsoluteCwd() + '/' + precinc
			localEnv.Append( CPPFLAGS = [ '/FI' + self.getRealAbsoluteCwd() + '/' + precinc, '/Zm135' ] )
			localEnv['PCH'] = localEnv.PCH( precsrc )[0]

		# create the target
		dstLib = localEnv.SharedLibrary( target=target, source=sourcesFiles )

		# explicitly create dependencies to all internal libraries used
		# i.e. internal libraries need to be compiled before this target
		internalLibsDepends = [ l.sconsNode for l in localLibraries if l.sconsNode ] # if there is a sconsNode inside the library it's an internal lib
		if internalLibsDepends:
			localEnv.Depends( dstLib, internalLibsDepends )

		dstLibInstall = dstLib
		if install:
			if installDir:
				dstLibInstall = localEnv.Install( installDir, dstLib )
			elif installAs:
				dstLibInstall = localEnv.InstallAs( installAs, dstLib[0] )
			else:
				dstLibInstall = localEnv.Install( self.inOutputLib(), dstLib )

		localEnv.Alias( target, dstLibInstall )
		localEnv.Alias( 'all', target )

		if self.windows:
			l_headers = self.scanFiles( l_dirs, accept=['*.h', '*.hpp', '*.tcc', '*.inl', '*.H'] ) + headers
			self.MSVSProject( target, dstLibInstall,
				sources = sourcesFiles,
				headers = l_headers, localHeaders=localHeaders,
				env = localEnv,
				)

		# expose this library
		envFlags=externEnvFlags
		self.appendDict( envFlags, globalEnvFlags )
		dstLibChecker = autoconf._internal.InternalLibChecker( lib=target, includes=self.prepareIncludes(l_includes), envFlags=envFlags, dependencies=localLibraries+dependencies, sconsNode=dstLibInstall )

		# add the new declared library to the list of libs checker in self.libs
		if public:
			if publicName:
				setattr(self.libs, publicName, dstLibChecker)
			else:
				setattr(self.libs, target, dstLibChecker)

		return dstLibInstall

	def Program( self, target,
			sources=[], dirs=[], libraries=[], includes=[],
			env=None, localEnvFlags={}, replaceLocalEnvFlags={}, externEnvFlags={}, globalEnvFlags={},
			dependencies=[], installDir=None, install=True,
			headers=[], localHeaders=[],
			accept=['*.cpp', '*.cc', '*.c'], reject=['@', '_qrc', '_ui', '.moc.cpp'] ):
		'''
		To create a program and expose it in the project to be simply used by other targets.

		target: name of the target file
		sources: list of source files
		dirs: list of directories that contains the sources files
		libraries: list of libraries
		includes: list of include directories
		env: you can specify your custom environment to create the library
		localEnvFlags: defines some flags locally
		replaceLocalEnvFlags: defines some flags locally
		externEnvFlags: defines some flags for external usage of the library (only other targets that use the current library will have these flags)
		globalEnvFlags: defines some flags
		dependencies: 
		installDir: Destination directory to install the target
		installAs: Full path of the fil to install
		install: install the target (in the default or custom dir or renamed using installAs)
		headers: headers to include in the project (not for build, but project generation eg. visualProject)
		localHeaders: headers to include in the project (not for build, but project generation eg. visualProject)
		accept: pattern to filter the source files search in @p dirs
		reject: pattern to filter the source files search in @p dirs
		public: If you declares the library as public, it can be used by other targets.
		'''
		l_sources = self.asList(sources)
		l_dirs = self.asList(dirs)
		l_libraries = self.asList(libraries)
		l_includes = self.asList(includes)
		sourcesFiles = []
		sourcesFiles += l_sources
		if l_dirs:
			sourcesFiles += self.scanFiles( l_dirs, accept, reject, inBuildDir=True )

		if not sourcesFiles:
			raise RuntimeError( "No source files for the target: " + target )
		
		localEnv = None
		localLibraries = l_libraries
		if env:
			localEnv = env.Clone()
			self.appendLibsToEnv(localEnv, localLibraries)
			if 'SconsProjectLibraries' in localEnv:
				localLibraries += localEnv['SconsProjectLibraries']
		else:
			# if no environment we create a new one
			localEnv = self.createEnv( localLibraries, name=target )

		# apply arguments to env
		localIncludes = self.prepareIncludes(l_dirs+l_includes)
		localEnv.AppendUnique( CPPPATH = localIncludes )
		if localEnvFlags:
			localEnv.AppendUnique( **localEnvFlags )
		if replaceLocalEnvFlags:
			localEnv.Replace( **replaceLocalEnvFlags )
		if globalEnvFlags:
			localEnv.AppendUnique( **globalEnvFlags )

		sourcesFiles = self.getAbsoluteCwd( sourcesFiles )
		
		# create the target
		dst = localEnv.Program( target=target, source=sourcesFiles )

		dstInstall = localEnv.Install( installDir if installDir else self.inOutputBin(), dst ) if install else dst
		localEnv.Alias( target, dstInstall )
		localEnv.Alias( 'all', target )

		if self.windows:
			l_headers = self.scanFiles( l_dirs, accept=['*.h', '*.hpp', '*.tcc', '*.inl', '*.H'] ) + headers
			self.MSVSProject( target, dstInstall,
				sources=sourcesFiles,
				headers=l_headers, localHeaders=localHeaders,
				env = localEnv,
				)

		return dstInstall


	def UnitTest( self, target=None, sources=[], dirs=[], env=None, libraries=[], includes=[], localEnvFlags={}, replaceLocalEnvFlags={},
	                         externEnvFlags={}, globalEnvFlags={}, dependencies=[],
	                         accept=['*.cpp', '*.cc', '*.c'], reject=['@', '_qrc', '_ui', '.moc.cpp'] ):
		'''
		To create a program and expose it in the project to be simply used by other targets.
		'''
		l_target = target
		if target is None:
			l_target = self.getDirs(0)
		l_sources = self.asList(sources)
		l_dirs = self.asList(dirs)
		l_libraries = self.asList(libraries)
		l_includes = self.asList(includes)

		if l_dirs:
			l_sources += self.scanFiles( l_dirs, accept, reject, inBuildDir=True )

		if not l_sources:
			raise RuntimeError( 'No source files for the target: ' + str(l_target) )
		
		localEnv = None
		localLibraries = l_libraries
		if env:
			localEnv = env.Clone()
			self.appendLibsToEnv(localEnv, localLibraries)
			if 'SconsProjectLibraries' in localEnv:
				localLibraries += localEnv['SconsProjectLibraries']
		else:
			# if no environment we create a new one
			localEnv = self.createEnv( localLibraries, name='-'.join(l_target) )

		# apply arguments to env
		localEnv.AppendUnique( CPPPATH = self.prepareIncludes(l_dirs+l_includes) )
		if localEnvFlags:
			localEnv.AppendUnique( **localEnvFlags )
		if replaceLocalEnvFlags:
			localEnv.Replace( **replaceLocalEnvFlags )
		if globalEnvFlags:
			localEnv.AppendUnique( **globalEnvFlags )

		# create the target
		dst = localEnv.UnitTest( target=l_target, source=l_sources )

		return dst

	def ScriptTests( self, target=None, sources=[], dirs=[], env=None, libraries=[], dependencies=[], envFlags={}, procEnvFlags={},
	                         accept=['test*.py'], reject=['@'] ):
		'''
		This target is a list of python script files to execute.
		'''
		l_target = target
		if target is None:
			l_target = self.getDirs(0)
		
		l_sources = self.asList(sources)
		l_dirs = self.asList(dirs)
		l_libraries = self.asList(libraries)
		l_dependencies = self.asList(dependencies)
		
		if l_dirs:
			l_sources += self.scanFiles( l_dirs, accept, reject, inBuildDir=True )

		if not l_sources:
			raise RuntimeError( 'No source files for the target: ' + str(l_target) )
		
		localEnv = None
		localLibraries = l_libraries
		if env:
			localEnv = env.Clone()
			if 'SconsProjectLibraries' in localEnv:
				localLibraries += localEnv['SconsProjectLibraries']
			self.appendLibsToEnv(localEnv, localLibraries)
		else:
			# if no environment we create a new one
			localEnv = self.createEnv( localLibraries, name='-'.join(l_target) )

		if envFlags:
			localEnv.AppendUnique( **envFlags )
		if procEnvFlags:
			for k, v in procEnvFlags.iteritems():
				localEnv.PrependENVPath( k, v )

		# create the target
		allDst = []
		for s in l_sources:
			dst = localEnv.ScriptTest( source=s, target=l_target )
			allDst.append(dst)

		return dst

#-------------------- Automatic file/directory search -------------------------#
	def asList(self, v):
		'''Return v inside a list if not a list.'''
		if isinstance(v, list):
			return v[:]
		if isinstance(v, tuple):
			return v[:]
		if isinstance(v, SCons.Node.NodeList):
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

	def scanFilesInDir(self, directory, accept, reject, recursive=True, inBuildDir=False):
		'''
		Recursively search files in 'directory' that matches 'accepts' wildcards and doesn't contain 'reject'
		'''
		l_accept = self.asList( accept )
		l_reject = self.asList( reject )
		sources = []
		realcwd = self.getRealAbsoluteCwd()
		paths = []
		dd = self.getRealAbsoluteCwd(directory)
		paths = self.recursiveDirs( dd ) if recursive else dd
		
		for path in paths:
			for pattern in l_accept:
				sources += Glob(os.path.join(path, pattern), strings=True) # string=True to return files as strings
		for pattern in l_reject:
			sources = filter((lambda a: a.rfind(pattern) == -1), sources)
		# to relative paths (to allow scons variant_dir to recognize files...)
		def toLocalDirs(d): return d.replace(realcwd + os.sep, '')
		lsources = self.inBuildDir(sources) if inBuildDir else map(toLocalDirs, sources)
		return self.unique(lsources)

	def scanFiles(self, dirs=['.'], accept=['*.cpp', '*.cc', '*.c'], reject=['@', '_qrc', '_ui', '.moc.cpp'], unique=True, recursive=True, inBuildDir=False):
		'''
		Recursively search files in "dirs" that matches 'accepts' wildcards and don't contains "reject"
		@param[in] unique Uniquify the list of files
		'''
		l_dirs = self.asList( dirs )
		files = []
		for d in l_dirs:
			files += self.scanFilesInDir(d, accept, reject, recursive, inBuildDir)
		if not unique:
			return files
		return self.unique(files)

	def dirnames(self, files):
		'''Returns the list of files dirname.'''
		dirs = self.unique(map(os.path.dirname, files))
		dirs.sort()
		return dirs

	def subdirsContaining(self, directory, patterns):
		'''
		Returns all sub directories of 'directory' containing a file matching 'patterns'.
		'''
		dirs = self.dirnames(self.scanFiles(directory, accept=patterns))
		dirs.sort()
		return dirs


__all__ = ['SConsProject']
