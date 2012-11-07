from SCons.Script.SConscript import SConsEnvironment

import os
import sys
import subprocess

windows = os.name.lower() == "nt" and sys.platform.lower().startswith("win")

ld_library_path = 'LD_LIBRARY_PATH' if not windows else 'PATH'
mpsep = ':' if not windows else ';'


def execute_UnitTest(target, source, env):
	'''
	Execute source param executable and create a file into target param.
	'''
	app = str(source[0].abspath)
	procenv = env['ENV']
	
	# Format LIBPATH to convert expressions into plain filepath
	ldPaths = []
	for p in env['LIBPATH']:
		pp = p.replace('#', env['TOPDIR']+'/')
		pEval = env.subst(pp)
		if pEval:
			ldPaths.append(pEval)
	procenv[ld_library_path] = mpsep.join(ldPaths)

	# Execute the test.
	errcode = subprocess.call(app, env=procenv)
	if errcode == 0:
		# Write something to the target file. It's just a fake file to keep a timestamp for file dependencies.
		open(str(target[0]), 'w').write("PASSED\n")
	return errcode


def UnitTest(env, source, **kwargs):
	'''
	Function added to the SCons Environment.
	Build an application from source files and run this executable as a Test.
	'''
	target = ['unittest']
	if 'target' not in kwargs:
		raise RuntimeError( 'No target for unittest.' )
	elif isinstance( kwargs['target'], list ):
		target.extend( kwargs['target'] )
	elif isinstance( kwargs['target'], str ):
		target.append( kwargs['target'] )
	else:
		raise RuntimeError( 'Target value not recognized:', kwargs['target'] )
	
	test = env.Program( target='-'.join( target ), source=source )
	
	unittest = env.ExecUnitTest( test[0].abspath+'.unittest_passed', test )
	
	# Build one alias for each element of the target list.
	for i in range(1,len(target)+1):
		env.Alias('-'.join(target[0:i]), unittest)

	return test


def generate(env):
	"""
	Add builders and construction variables for unittest.
	"""
	import SCons.Builder
	unitTestExecute = SCons.Builder.Builder(action = execute_UnitTest)
	env.Append(BUILDERS = {'ExecUnitTest' : unitTestExecute })

	SConsEnvironment.UnitTest = UnitTest


def exists(env):
	return True


