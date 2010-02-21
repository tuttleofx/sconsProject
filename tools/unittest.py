from SCons.Script.SConscript import SConsEnvironment

import os

#
# Function taken from scons Wiki
#
def builder_unit_test(target, source, env):
	app = str(source[0].abspath)
	if os.spawnl(os.P_WAIT, app, app) == 0:
		open(str(target[0]), 'w').write("PASSED\n")
	else:
		return 1


def UnitTest(env, source, **kwargs):
    if 'target' in kwargs:
        kwargs['target'] = 'unittest-'+kwargs['target']
    test = env.Program(source=source, **kwargs)
    unittest = env.Test( test[0].abspath+'.unittest_passed', test )
    if 'target' in kwargs:
        env.Alias(kwargs['target'], unittest)
    env.Alias('unittest', unittest)
    return test



def generate(env):
    """
    Add builders and construction variables for unittest.
    """
    import SCons.Builder
    unitTestBuilder = SCons.Builder.Builder(action = builder_unit_test)
    env.Append(BUILDERS = {'Test' : unitTestBuilder })
    
    SConsEnvironment.UnitTest = UnitTest


def exists(env):
    return True


