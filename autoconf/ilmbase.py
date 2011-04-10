from _external import *
from pthread import *

ilmbase = LibWithHeaderChecker(
		['Imath', 'Half', 'Iex', 'IlmThread'],
		['OpenEXR/Iex.h', 'OpenEXR/IlmBaseConfig.h', 'OpenEXR/ImathVec.h', 'OpenEXR/half.h'],
		'c++',
		name='ilmbase',
		dependencies=[pthread],
	    )


