from _external import *
from boost import *

class BoostUnittestframeworkChecker(BaseLibChecker):

    def __init__( self ):
        self.name  = 'boost_unittestframework'
        self.language = 'c++',
        self.dependencies=[boost]

    def initOptions(self, project, opts):
        opts.Add( Variables.BoolVariable( 'with_'+self.name, 'enabled compilation with '+self.name, True  ) )
        return True

    def configure(self, project, env):
        if not self.enabled(env):
            return True
        env.Append( CCFLAGS = project.CC['define']+'BOOST_TEST_DYN_LINK' )
        return True

    def check(self, project, conf):
        result = self.CheckLib(conf, 'boost_unit_test_framework' ) #, None, None, self.language)
        #or result = self.CheckLib(conf, 'boost_unit_test_framework' ) #, None, None, self.language)
        self.checkDone = True
        return result


boost_unittestframework = BoostUnittestframeworkChecker()

