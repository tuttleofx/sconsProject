from _external import *
from util import *
from dl import *

python = LibWithHeaderChecker('python',
                              'Python.h',
                              'c',
                              name='python',
                              dependencies = [util, dl]
                              )


