from _external import *
from ilmbase import *

ctl = LibWithHeaderChecker(
		['IlmCtlSimd', 'IlmCtl', 'IlmCtlMath'],
		['CtlSimdInterpreter.h','Iex.h'],
		'c++',
		name='ctl',
		call='Ctl::SimdInterpreter interp; interp.setMaxInstCount(10);',
		dependencies=[ilmbase],
	    )


