from _external import *
from boost_filesystem import *
from boost_regex import *
from boost_system import *
from boost_thread import *
from openjpeg import *
from half import *
from dl import *

openimageio = LibWithHeaderChecker(
            ['OpenImageIO'], 'imageio.h', 'c++',
            name='openimageio',
            call='',
            dependencies = [
                boost_filesystem,
                boost_regex,
                boost_system,
                boost_thread,
                openjpeg,
                half,
                dl] )


