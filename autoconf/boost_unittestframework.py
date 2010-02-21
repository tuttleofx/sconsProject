from base import *

class BoostUnittestframeworkChecker(BaseLibChecker):

    def __init__( self ):
        self.name  = 'boost_unittestframework'
        self.language = 'c++'
        pass

    def initOptions(self, putois, opts):
        opts.Add( Variables.BoolVariable( 'with_'+self.name, 'enabled compilation with '+self.name, True  ) )
        return True

    def configure(self, putois, env):
        if not self.enabled(env):
            return True
        env.Append( CCFLAGS = putois.CC['define']+'BOOST_TEST_DYN_LINK' )
        return True

    def check(self, conf):
        if not self.enabled(conf.env):
            return True
        result = self.CheckLib(conf, 'boost_unit_test_framework' ) #, None, None, self.language)
        #or result = self.CheckLib(conf, 'boost_unit_test_framework' ) #, None, None, self.language)
        self.checkDone = True
        return result


boost_unittestframework = BoostUnittestframeworkChecker()

