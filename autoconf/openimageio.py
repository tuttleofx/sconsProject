from _external import *
from boost_filesystem import *
from boost_regex import *
from boost_system import *
from boost_thread import *
from openjpeg import *
from half import *
from dl import *
from tiff import *
from webp import *
from raw import *
from z import *
from ilmbase import *
from openexr import *
from png import *
from gif import *

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
                dl,
                tiff,
                webp,
                raw,
                z,
                openexr,
                ilmbase,
                png,
                gif
                ] )


