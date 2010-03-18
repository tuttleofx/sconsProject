from _external import *

openexr = LibWithHeaderChecker(
            ['IlmImf', 'Half', 'IlmThread'], 'OpenEXR/ImfInputFile.h', 'c++',
            name='openexr',
            call='Imf::InputFile("test.exr");')


