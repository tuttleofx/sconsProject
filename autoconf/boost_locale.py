from _external import *
from boost import *
from boost_system import *


boost_locale = LibWithHeaderChecker(
        'boost_locale',
        ['boost/locale.hpp'],
        'c++',
        dependencies = [boost, boost_system],
    )

