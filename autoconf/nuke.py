from _external import *
from glew import *
from pthread import *

nuke = LibWithHeaderChecker( ['DDImage'],
                             ['iostream','DDImage/NukeWrapper.h','Build/fnBuild.h'],
                             language='c++',
                             name='nuke',
                             dependencies=[glew, pthread] )
