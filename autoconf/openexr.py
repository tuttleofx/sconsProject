from base import *

openexr = LibWithHeaderChecker(
            'IlmImf', 'ImfInputFile.h', 'c++', name='openexr',
            call='Imf::InputFile("test.exr");')


