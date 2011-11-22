from _external import *
from boost import *
from qt4 import *

qxorm = LibWithHeaderChecker(
	'QxOrm',
	'QxOrm.h',
	'c++',
	name='qxorm',
	dependencies= [ boost, qt4(modules=[ 'QtCore', 'QtGui', 'QtSql' ] ) ],
	)

