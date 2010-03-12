
from SCons.Environment import *
from SCons.Script import *

from utils import *
from utils.colors import *
import compilators
import autoconf

import os
import sys
import atexit
from time import *
import socket # to get hostname
import string


class SConsProject:
    '''
    This is a base class helper for SCons build tool.
    In your SConstruct simply do:

    from sconsProject import SConsProject

    project = SConsProject()
    libs = project.libs
    Export('project')
    Export('libs')

    project.begin()
    project.SConscript()
    project.end()

    # If you have common creation things in your project, create a class for your project which inherite this class.
    # So this function is accessible in all SConscript.
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

    # and just replace
    project = MyProject()
    '''
    now               = strftime("%Y-%m-%d_%Hh%Mm%S", localtime())
    osname            = os.name.lower()
    sysplatform       = sys.platform.lower()
    hostname          = socket.gethostname()
    compil_mode       = 'unknown_mode'
    dir               = os.getcwd()
    dir_build_name    = '.dist'                   # base dir name for all intermediate compilation objects
    dir_output_name   = 'dist'                    # base dir name for output build
    dir_output_build  = 'undefined'               # 
    dir_output_bin    = 'undefined'               # name generated depending on compilation type,
    dir_output_lib    = 'undefined'               # we need to know if we are in debug mode, etc.
    dir_output_header = 'undefined'               # (options needs to be initilized)
    dir_output_test   = 'undefined'               #
    dir_sconsProject  = os.path.abspath(os.path.dirname(__file__)) # directory containing this file
    
    compilator        = ""
    libs              = autoconf
    commonLibs        = [libs.sconsProject]
    libs_help         = [] # temporary list which contains all librairies already added to help
    libs_error        = [] # list of libraries with autoconf error
    env               = Environment(tools=['default', 'packaging', 'doxygen', 'unittest',
                                           'qt4'], toolpath=[dir_sconsProject+"/tools"])

    def __init__( self ):
        if self.osname == "nt" :
            self.packagetype    = 'msi'
        else :
            self.packagetype    = 'rpm'

        if self.osname == "posix" :
            if (os.uname()[4][-3:] == '_64'):
                self.bits = 64
            else:
                self.bits = 32
        elif self.osname == "nt":
            self.bits = 32
            
        self.sconf_files  = [os.path.join(self.dir_sconsProject,'hostconf.py'), os.path.join(self.dir,'hostconf.py'), os.path.join(self.dir,self.hostname+'.py')]
        
        # scons optimizations...
        self.env.SourceCode('.', None)
        self.env.Decider('MD5-timestamp')
        SetOption('implicit_cache', 1)
        SetOption('max_drift', 60*15) # cache the checksum after max_drift seconds

    
    #------------------------------------ Utils -----------------------------------#
    def printInfos( self ):
        sys.stdout.write( self.env['color_info'] )
        print ':'*80
        print ':'*33, self.env['mode'], 'mode', ':'*33
        print ':'*80
        print ':: dir                = '+ self.dir
        print ':: dir_output_build   = '+ self.dir_output_build
        print ':: dir_output_bin     = '+ self.dir_output_bin
        print ':: dir_output_lib     = '+ self.dir_output_lib
        print ':: dir_output_test    = '+ self.dir_output_test
        print ':: dir_sconsProject   = '+ self.dir_sconsProject
        print ':: now                = '+ self.now
        print ':: osname             = '+ self.osname
        print ':: sysplatform        = '+ self.sysplatform
        print ':: hostname           = '+ self.hostname
        print ':: compilator c++     = '+ self.env['CXX']
        if 'CCVERSION' in self.env :
            print( ':: compilator version = '+ self.env['CCVERSION'] )
        print( ':: parallel jobs      = %d' % (GetOption('num_jobs')) )
        print( ':'*80 )
        sys.stdout.write( self.env['color_clear'] )

    def printEnv( self, env=None, keys=[] ) :
        if not env :
            print ':'*20, ' env ', ':'*20
            env = self.env
        if not keys :
            sys.stdout.write( self.env['color_info'] )
            print env.Dump()
        else :
            print '*'*50, 'keys: ', keys
            dict = env.Dictionary()
            for key in keys :
                if key in dict :
                    sys.stdout.write( self.env['color_info'] )
                    print ':'*10, ' %s = %s' % (key, dict[key])
        sys.stdout.write( self.env['color_clear'] )

    def getRealAbsoluteCwd( self, relativePath=None ) :
        '''Returns original current directory (not inside the VariantDir)...'''
        dir = Dir('.').srcnode().abspath
        if relativePath:
            return os.path.join( dir, relativePath )
        else:
            return dir

    def getAbsoluteCwd( self, relativePath=None ) :
        '''Returns current directory...'''
        dir = Dir('.').abspath
        if relativePath:
            return os.path.join( dir, relativePath )
        else:
            return dir

    def getSubDirsAbsolutePath( self , current_dir=None) :
        '''Returns sub-directories with absolute paths (in original file tree).'''
        if current_dir==None : 
            current_dir =  self.getRealAbsoluteCwd()
        else :
            current_dir = Dir('./'+current_dir).srcnode().abspath
        
        files = (os.listdir( current_dir )) # relative paths (only directories names)
        #files.append(current_dir)
        nonhidden = (f for f in files if f[0]!='.' and f.find('@') )
        absfiles = ( os.path.join(current_dir, f) for f in nonhidden ) # absolute paths
        dirs = ( f for f in absfiles if os.path.isdir(f) )
        return dirs

    def getSubDirs( self , current_dir=None) :
        '''Returns sub-directories with relative paths (in original file tree).'''
        return map( os.path.basename, self.getSubDirsAbsolutePath(current_dir) ) # absolute path -> relative path (for variant_dir)

    def getSubDirsWithSConscript( self ) :
        '''Returns sub-directories containing a SConscript file with relative paths (in original file tree).'''
        alldirs = self.getSubDirsAbsolutePath()
        dirs = ( f for f in alldirs if os.path.isfile( os.path.join(f,'SConscript') ) )
        ldirs = map( os.path.basename, dirs ) # absolute path -> relative path (for variant_dir)
        return ldirs

    def inBuildDir( self, *dirs ):
        if not dirs:
            return string.replace( os.getcwd(), self.dir, self.dir_output_build )
        return [string.replace( d, self.dir, self.dir_output_build ) for d in dirs]

    def inTopDir( self, *dirs ) :
        '''Returns "dirs" as subdirectories of "topDir".'''
        basedir = self.dir + os.sep
        if not dirs:
            return basedir
        return [basedir + d for d in dirs]
    
    def inOutputLib( self, *dirs ) :
        '''Returns "dirs" as subdirectories of "outputLib".'''
        basedir = self.dir_output_lib + os.sep
        if not dirs:
            return basedir
        return [basedir + d for d in dirs]

    def inOutputHeaders( self, *dirs ) :
        '''Returns "dirs" as subdirectories of "outputHeaders".'''
        basedir = self.dir_output_header + os.sep
        if not dirs:
            return basedir
        return [basedir + d for d in dirs]

    def inOutputBin( self, *dirs ) :
        '''Returns "dirs" as subdirectories of "outputBin".'''
        basedir = self.dir_output_bin + os.sep
        if not dirs:
            return basedir
        return [basedir + d for d in dirs]

    def inOutputTest( self, *dirs ) :
        '''Returns "dirs" as subdirectories of "outputTest".'''
        basedir = self.dir_output_test + os.sep
        if not dirs:
            return basedir
        return [basedir + d for d in dirs]

    def getName( self ) :
        '''Returns the current directory, often used as name.'''
        return os.path.basename( os.getcwd() )

    def needConfigure(self):
        '''If the target builds nothing, we don't need to call the configure function.'''
        return not GetOption( 'clean' ) and not GetOption( 'help' )
    
    #------------------------- Compilation options ----------------------------#
    def initOptions( self ):
        '''
        Read options from configuration files and at last from the command line
        (which has the last word)
        '''
        if self.osname == "nt" and self.sysplatform.startswith("win"):
            self.win           = True
            self.compilator    = 'visualc'
            self.ccompilator   = 'cl'
            self.cxxcompilator = 'cl'
            self.CC            = compilators.visual.CC
        else:
            self.win           = False
            self.compilator    = 'gnugcc'
            self.ccompilator   = 'gcc'
            self.cxxcompilator = 'g++'
            self.CC            = compilators.gcc.CC
        
        # options from command line or configuration file
        self.opts = self.createOptions( self.sconf_files, ARGUMENTS )
        self.opts_help = self.createOptions( self.sconf_files, ARGUMENTS )
        self.defineHiddenOptions( self.opts )
        
        self.opts.Update( self.env )
    
    def createOptions( self, filename, args ):
        '''
        Define basics options.
        '''
        opts = Variables( filename, args )

        def help_format(env, opt, help, default, actual, aliases):
            return '%s%s%s\n\t%s\n\t( default=%s, actual=%s)\n\n' % (self.env['color_title'], opt, self.env['color_clear'], help, default, actual)
        opts.FormatVariableHelpText = help_format
        
        opts.Add( EnumVariable( 'mode',          'Compilation mode',                                'debug', allowed_values=('debug', 'release', 'dist') ) )
        opts.Add( BoolVariable( 'install',       'Install',                                         False ) )
        opts.Add( BoolVariable( 'profile',       'Build with profiling support',                    False ) )
        opts.Add( BoolVariable( 'cover',         'Build with cover support',                        False ) )
        opts.Add( BoolVariable( 'clean',         'Remove all the build directory',                  False ) )
        opts.Add( BoolVariable( 'ignore_errors', 'Ignore any configuration errors',                 False ) )
        opts.Add( BoolVariable( 'log',           'Enable output to a log file',                     False ) )
        opts.Add( BoolVariable( 'ccache',        'Enable compilator cache system (ccache style)',   True  ) )
        opts.Add( BoolVariable( 'colors',        'Using colors of the terminal',                    True  ) )
        opts.Add( 'jobs',                        'Parallel jobs',                                   '1' )
        opts.Add( 'CC',                          'Specify the C Compiler',                          self.ccompilator )
        opts.Add( 'CXX',                         'Specify the C++ Compiler',                        self.cxxcompilator )
        
        opts.Add( PathVariable( 'ENVINC',        'Additional include path (at compilation)',   '',  PathVariable.PathAccept ) )
        opts.Add( PathVariable( 'ENVPATH',       'Additional bin path (at compilation)',       '',  PathVariable.PathAccept ) )
        opts.Add( PathVariable( 'ENVLIBPATH',    'Additional librairie path (at compilation)', '',  PathVariable.PathAccept ) )

        opts.Add( 'CCPATH',     'Additional preprocessor paths', [] )
        opts.Add( 'CPPPATH',    'Additional preprocessor paths', [] )
        opts.Add( 'LIBPATH',    'Additional library paths',      [] )
        opts.Add( 'CCFLAGS',    'Additional C++ flags',          [] )
        opts.Add( 'CPPFLAGS',   'Additional C++ flags',          [] )
        opts.Add( 'CCDEFINES',  'Additional constants',          [] )
        opts.Add( 'CPPDEFINES', 'Additional constants',          [] )
        opts.Add( 'LIBS',       'Additional libraries',          [] )
        # Don't explicitly put include directory arguments in CCFLAGS or CXXFLAGS
        # because the result will be non-portable and the directories will not
        # be searched by the dependency scanner.
        opts.Add( 'CCFLAGS',    'Additional C flags',            [] )
        opts.Add( 'CPPFLAGS',   'Additional C flags',            [] )
        opts.Add( 'LINKFLAGS',  'Additional linker flags',       [] )
        
        opts.Add( PathVariable( 'EXTLIBRARIES', 'Directory of external libraries',         '.',      PathVariable.PathAccept      ) )
        opts.Add( PathVariable( 'BUILDDIR',     'Top directory of compilation tree',       self.dir, PathVariable.PathIsDirCreate ) )
        opts.Add( PathVariable( 'BINDIR',       'Top directory for output compiled files', self.dir, PathVariable.PathIsDirCreate ) )
        opts.Add( PathVariable( 'INSTALLDIR',   'Top directory to install compiled files', os.path.join(self.dir,self.dir_output_name), PathVariable.PathIsDirCreate ) )
        
        return opts

    def defineHiddenOptions( self, opts ):
        '''
        Define basics options which don't need to be visible in the help.
        '''
        
        opts.Add( BoolVariable( 'visual',      'Compilator',           True ) )
        opts.Add( PathVariable( 'TOPDIR',      'Top directory',        self.dir ) )
        opts.Add( BoolVariable( 'check_libs',  'Disable lib checking', True ) )
        
        opts.Add( 'OSBITS', 'OS bits', self.bits )
        opts.Add( BoolVariable( 'UNIX',    'operating system', not self.win ) )
        opts.Add( BoolVariable( 'WINDOWS', 'operating system', self.win     ) )
        
        opts.Add( 'osname', 'OS name', 'windows' if self.win else 'unix' )
        
        # display options
        opts.Add( 'SHCCCOMSTR',          'display option', '$SHCCCOM' )
        opts.Add( 'SHCXXCOMSTR',         'display option', '$SHCXXCOM' )
        opts.Add( 'SHLINKCOMSTR',        'display option', '$SHLINKCOM' )
        opts.Add( 'CCCOMSTR',            'display option', '$CCCOM' )
        opts.Add( 'CXXCOMSTR',           'display option', '$CXXCOM' )
        opts.Add( 'LINKCOMSTR',          'display option', '$LINKCOM' )
        opts.Add( 'ARCOMSTR',            'display option', '$ARCOM' )
        opts.Add( 'INSTALLSTR',          'display option', 'Install file: $SOURCE as $TARGET' )
        opts.Add( 'SWIGCOMSTR',          'display option', '$SWIGCOM' )
        opts.Add( 'QT_MOCFROMCXXCOMSTR', 'display option', '$QT_MOCFROMCXXCOM' )
        opts.Add( 'QT_MOCFROMHCOMSTR',   'display option', '$QT_MOCFROMHCOM' )
        opts.Add( 'QT_UICCOMSTR',        'display option', '$QT_UICCOM' )
        
        opts.Add( 'color_clear',     'color', colors['clear'] )
        opts.Add( 'color_red',       'color', colors['red'] )
        opts.Add( 'color_redB',      'color', colors['redB'] )
        opts.Add( 'color_green',     'color', colors['green'] )
        opts.Add( 'color_blue',      'color', colors['blue'] )
        opts.Add( 'color_blueB',     'color', colors['blueB'] )
        opts.Add( 'color_yellow',    'color', colors['yellow'] )
        opts.Add( 'color_brown',     'color', colors['brown'] )
        opts.Add( 'color_violet',    'color', colors['violet'] )

        opts.Add( 'color_autoconf',  'color', '' )
        opts.Add( 'color_header',    'color', '' )
        opts.Add( 'color_title',     'color', '' )
        opts.Add( 'color_compile',   'color', '' )
        opts.Add( 'color_link',      'color', '' )
        opts.Add( 'color_install',   'color', '' )

        opts.Add( 'color_info',      'color', '' )
        opts.Add( 'color_success',   'color', '' )
        opts.Add( 'color_warning',   'color', '' )
        opts.Add( 'color_fail',      'color', '' )
        opts.Add( 'color_error',     'color', colors['error'] )


    def applyOptionsOnProject( self ):
        
        if self.env['install']:
            self.env['mode'] = 'dist'
        self.dir_output_build  = os.path.join( self.env['BUILDDIR'], self.dir_build_name, self.hostname, self.env['mode'])
        install_dir = os.path.join( self.env['BINDIR'], self.dir_output_name, self.hostname, self.env['mode'] )
        if self.env['install']:
            install_dir = self.env['INSTALLDIR']
        self.dir_output_bin    = os.path.join( install_dir, 'bin' )
        self.dir_output_lib    = os.path.join( install_dir, 'lib' )
        self.dir_output_header = os.path.join( install_dir, 'include' )
        self.dir_output_test   = os.path.join( install_dir, 'test' )
        
        # temporary files of SCons inside the build directory
        self.env['CONFIGUREDIR'] = os.path.join( self.dir_output_build, 'sconf_temp' )
        self.env['CONFIGURELOG'] = os.path.join( self.dir_output_build, 'config.log' )
        SConsignFile( os.path.join( self.dir_output_build, 'sconsign.dblite') )
        
        if self.env['ccache']:
            CacheDir( self.dir_output_build + os.sep + 'ccache' )

    	try:
        	SetOption('num_jobs', int(self.env['jobs']))
    	except:
        	pass

        self.applyOptionsOnEnv( self.env )
    
    
    def applyOptionsOnEnv( self, env ):
        
        env.PrependENVPath('INCLUDE', self.env['ENVINC'])
        env.PrependENVPath('PATH',    self.env['ENVPATH'])
        env.PrependENVPath('LIB',     self.env['ENVLIBPATH'])
        
        if not env['colors']:
            for c in ['color_clear','color_red','color_redB','color_green','color_blue','color_blueB','color_yellow','color_brown','color_violet','color_autoconf','color_header','color_title','color_compile','color_link','color_install','color_info','color_success','color_warning','color_fail','color_error']:
                env[c]=''


    def begin(self):
        
        self.initOptions()
        self.applyOptionsOnProject()
        
        if self.env['clean']:
            Execute(Delete( self.dir_output_build ))
            Execute(Delete( self.dir_output_bin ))
            Execute(Delete( self.dir_output_lib ))
            Execute(Delete( self.dir_output_test ))
            Exit(1)

        self.printInfos()
        
        VariantDir( self.dir_output_build, self.dir, duplicate=0 )


    def end(self):

        # by default compiles the target 'all'
        Default( 'all' )
        
        doxygen = self.env.Doxygen( self.inTopDir('doc/config/Doxyfile') )
        
        self.env.Alias( 'doc', doxygen )
        self.env.Alias( 'doxygen', doxygen )
        self.env.Clean( doxygen, ['doc/html'])


        if self.libs_error:
            sys.stdout.write( self.env['color_error'] )
            for lib in self.libs_error:
                print "Error in '"+lib.name+"' library :"
                if lib.error:
                    print '\t', lib.error
            sys.stdout.write( self.env['color_clear'] )
            if not self.env['ignore_errors']:
                #raise 'BuildError', 'Configure errors... Compilation STOP !'
                print 'Configure errors... Compilation STOP !'
                print 'Use ignore_errors=1 to try to compile without correcting the problem.'
                Exit(1)
            sys.stdout.write( self.env['color_clear'] )

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
        
        Help( self.opts_help.GenerateHelpText( self.env ) )

        # register function to display compilation status at the end
        # to avoid going through if SCons raises an exception (error in a SConscript)
        atexit.register(utils.display_build_status)
        
        
    #-------------------------------- Autoconf ------------------------------------#
    
    def createEnv( self, libs=[] ):
        '''
        Create an environment from the common one and apply libraries configuration to this environment.
        @todo : add opts=[] ?
        '''
        sys.stdout.write( self.env['color_autoconf'] ) # print without new line
        env_current = self.env.Clone()
        
        for lib in self.commonLibs:
            libs.insert( 0, lib ) # prepend (self.libs.sconsProject)
        opts_current = self.createOptions( self.sconf_files, ARGUMENTS )
        for eachlib in libs:
            for lib in eachlib.dependencies + [eachlib] :
                self.defineHiddenOptions( opts_current )
                if not lib.initOptions(self,opts_current):
                    if lib not in self.libs_error:
                        self.libs_error.append( lib )
                if lib not in self.libs_help:
                    lib.initOptions(self,self.opts_help)
                    self.libs_help.append( lib )
        opts_current.Update(env_current)
        self.applyOptionsOnEnv(env_current)
        
        if self.needConfigure():
            conf = env_current.Configure()
            for eachlib in libs:
                for lib in eachlib.dependencies + [eachlib] :
                    if not lib.configure(self,env_current):
                        if lib not in self.libs_error:
                            self.libs_error.append( lib )
                    #elif self.env['check_libs']:
                    elif not lib.check(conf):
                        if lib not in self.libs_error:
                            self.libs_error.append( lib )
            env_current = conf.Finish()
        
        for eachlib in libs:
            for lib in eachlib.dependencies + [eachlib]:
                lib.postconfigure(self,env_current)
        
        sys.stdout.write( self.env['color_clear'] )
        return env_current

# todo
#    def Install(self):
#        
#        env.AddPostAction(obj , Chmod(str(obj),bin_mode) )

    #------------------- Automatic file search ------------------------#
    def recursiveDirs( self, root ) :
        return filter( (lambda a : a.rfind("CVS")==-1 ),  [ a[0] for a in os.walk(root)]  )

#    def unique( self, sourcesList ) :
#        # element order not preserved
#        return dict.fromkeys(sourcesList).keys()

    def unique( self, sourcesList ):
        # element order preserved
        unique_trick = [uniq for uniq in sourcesList if uniq not in locals()['_[1]']]
        return unique_trick

    def scanFilesInDir( self, directory, accept, reject) :
        '''
        Recursively search files in "directory" that matches 'accepts' wildcards and don't contains "reject"
        '''
        sources = []
        realcwd = self.getRealAbsoluteCwd()
        # on passe en absolu pour parcourir les fichiers
        absdir = realcwd + os.sep + directory
        paths = self.recursiveDirs( absdir )
        for path in paths :
            for pattern in accept :
                sources += Glob( os.path.join(path, pattern), strings=True ) # string=True to return files as strings
        for pattern in reject :
            sources = filter( (lambda a : a.rfind(pattern)==-1 ),  sources )
        # to relative paths (to allow scons variant_dir to recognize files...)
        def toLocalDirs(d) : return d.replace( realcwd + os.sep, '' )
        lsources = map( toLocalDirs, sources )
        return self.unique( lsources )

    def scanFiles( self, dirs=['.'], accept=['*.cpp','*.c'], reject=['@','_qrc', '_ui', '.moc.cpp'] ) :
        '''
        Recursively search files in "dirs" that matches 'accepts' wildcards and don't contains "reject"
        '''
        files = []
        for d in dirs:
            files += self.scanFilesInDir( d, accept, reject )
        return files
        
    def subdirs(self,files):
        dirs = self.unique(map(os.path.dirname, files))
        dirs.sort()
        return dirs

    def subdirsContaining(self,dir, patterns):
        dirs = self.subdirs(self.scanFiles(dir, accept=patterns))
        dirs.sort()
        return dirs


__all__ = ['SConsProject']

