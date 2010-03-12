from base import *

openexr = LibWithHeaderChecker(
            'IlmImf', 'OpenEXR/ImfInputFile.h', 'c++', name='openexr',
            call='Imf::InputFile("test.exr");')


