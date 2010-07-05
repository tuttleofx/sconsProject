from _external import *
from glew import *
from pthread import *

nuke = LibWithHeaderChecker( ['DDImage'],
                             ['cstdarg','memory','iostream','DDImage/NukeWrapper.h','Build/fnBuild.h'],
                             language='c++',
                             name='nuke',
                             dependencies=[glew, pthread] )
