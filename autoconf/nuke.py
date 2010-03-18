from _external import *

from glew import glew


class NukeChecker(LibWithHeaderChecker):

    def __init__( self ):
	self.name  = 'nuke'
	self.dependencies = [glew]
	#if windows:
	#    self.nukelib = 'DDImage5.0'
	#else:
	self.nukelib = 'DDImage'

    def check(self, conf):
	if not self.enabled(conf.env):
	    return True
		#GLEW
	return self.CheckLibWithHeader( conf, [self.nukelib], header=['iostream','DDImage/NukeWrapper.h','Build/fnBuild.h'], language='c++' )

nuke = NukeChecker()
