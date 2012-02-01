from _external import *
from boost import *
from boost_serialization import *
from qt4 import *

qxorm = LibWithHeaderChecker(
	'QxOrm',
	'QxOrm.h',
	'c++',
	name='qxorm',
	dependencies= [ boost, boost_serialization, qt4(modules=[ 'QtCore', 'QtGui', 'QtSql' ] ) ],
	)

