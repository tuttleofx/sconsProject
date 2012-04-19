from _external import *
from pthread import *
from half import *

ilmbase = LibWithHeaderChecker(
		['Imath', 'Iex', 'IlmThread'],
		['OpenEXR/Iex.h', 'OpenEXR/IlmBaseConfig.h', 'OpenEXR/ImathVec.h'],
		'c++',
		name='ilmbase',
		dependencies=[pthread, half],
	    )


