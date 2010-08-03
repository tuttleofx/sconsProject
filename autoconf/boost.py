from _external import *

class BoostChecker(HeaderChecker):
    '''
    TODO
    '''

    def __init__( self, version ):
        HeaderChecker.__init__( 'boost', ['boost/static_assert.hpp'], 'c++' )

    def checkVersion(self,context,version):
        # Boost versions are in format major.minor.subminor
        v_arr = version.split(".")
        version_n = 0
        if len(v_arr) > 0:
            version_n += int(v_arr[0])*100000
        if len(v_arr) > 1:
            version_n += int(v_arr[1])*100
        if len(v_arr) > 2:
            version_n += int(v_arr[2])

        context.Message('Checking for Boost version >= %s... ' % (version))
        #ret = context.TryRun("""
        ret = context.TryCompile("""
        #include <boost/version.hpp>

        int main()
        {
            return BOOST_VERSION >= %d ? 0 : 1;
        }
        """ % version_n, '.cpp')[0]
        context.Result(ret)
        return ret

    def check(self, project, conf):
        # self.checkVersion()
        return True

#boost = BoostChecker()
boost = HeaderChecker( 'boost',['boost/static_assert.hpp'], 'c++' )

