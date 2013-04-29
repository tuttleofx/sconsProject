from _external import *
from glib import *

gobject = LibWithHeaderChecker('gobject','glib-object.h','c', dependencies=[ glib ] )

