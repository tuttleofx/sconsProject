from _external import *
from sqlpp11 import *


sqlpp11_postgresql = LibWithHeaderChecker( 'sqlpp11_postgresql', 'sqlpp11/postgresql/postgresql.h', 'c++', dependencies=[sqlpp11] )

