from _external import *
from ilmbase import *
from z import *

openexr = LibWithHeaderChecker(
		['IlmImf'],
		'OpenEXR/ImfInputFile.h',
		'c++',
		name='openexr',
		call='Imf::InputFile("test.exr");',
		dependencies=[ilmbase,z],
	    )


