from SCons.Script.SConscript import SConsEnvironment

import os
import sys
import warnings
with warnings.catch_warnings():
	warnings.simplefilter("ignore")
	import subprocess32

windows = os.name.lower() == "nt" and sys.platform.lower().startswith("win")

ld_library_path = 'LD_LIBRARY_PATH' if not windows else 'PATH'
mpsep = ':' if not windows else ';'


def execute_ScriptTest(target, source, env):
	'''
	Execute source param executable and create a file into target param.
	'''
	app = str(source[0].abspath)
	outputFilename = str(target[0])
	procenv = env['ENV']
	
	# Format LIBPATH to convert expressions into plain filepath
	ldPaths = []
	for p in env['LIBPATH']:
		pp = p.replace('#', env['TOPDIR']+'/')
		pEval = env.subst(pp)
		if pEval:
			ldPaths.append(pEval)
	procenv[ld_library_path] = mpsep.join(ldPaths)

	writingFilename = outputFilename + "-writing"
	failedFilename = outputFilename + "-failed"

	# clean before the new build
	if os.path.exists(outputFilename):
		os.remove(outputFilename)
	if os.path.exists(writingFilename):
		os.remove(writingFilename)
	if os.path.exists(failedFilename):
		os.remove(failedFilename)

	cmd = [env['SCRIPTTESTXX'], app] + env['SCRIPTTESTFLAGS'].split(' ')

	print( ' '.join(cmd) )

	# Execute the test.
	errcode = 0
	with open(writingFilename, 'w') as writingFile:
		try:
			errcode = subprocess32.call(cmd, env=procenv, stdout=writingFile, stderr=subprocess32.STDOUT, timeout=60)
		except subprocess32.TimeoutExpired as e:
			writingFile.write( "scriptttest timeout expired: " + str(e) )
			print("scriptttest timeout expired.")
			errcode = -1

	for line in open(writingFilename, 'r').readlines():
		sys.stdout.write( "    " + line )

	# We use a fake file to keep a timestamp for file dependencies.
	# We keep the log inside this file.
	if errcode == 0:
		# The test is passed with success.
		# We rename the log file to the output dependence filename,
		# so the test will seen has done by scons, and
		# will not be executed again.
		os.rename(writingFilename, outputFilename)
	else:
		# the failed file is not the output dependence
		os.rename(writingFilename, failedFilename)
	return errcode


def ScriptTest(env, source, **kwargs):
	'''
	Function added to the SCons Environment.
	Build an application from source files and run this executable as a Test.
	'''
	target = ['scripttest']
	if 'target' not in kwargs:
		raise RuntimeError( 'No target for scripttest.' )
	elif isinstance( kwargs['target'], list ):
		target.extend( kwargs['target'] )
	elif isinstance( kwargs['target'], str ):
		target.append( kwargs['target'] )
	else:
		raise RuntimeError( 'Target value not recognized:', kwargs['target'] )
	
	scripttest = env.ExecScriptTest( source+'.scripttest', source )
	
	fileBaseName = os.path.splitext(os.path.basename(source))[0]
	env.Alias( '-'.join(['scripttest', fileBaseName]), scripttest )

	target.append(fileBaseName)
	# Build one alias for each element of the target list.
	for i in xrange(1,len(target)+1):
		env.Alias('-'.join(target[0:i]), scripttest)

	return scripttest


def generate(env):
	"""
	Add builders and construction variables for scripttest.
	"""
	import SCons.Builder
	scriptTestExecute = SCons.Builder.Builder(action = execute_ScriptTest)
	env.Append(BUILDERS = {'ExecScriptTest' : scriptTestExecute })

	SConsEnvironment.ScriptTest = ScriptTest


def exists(env):
	return True


