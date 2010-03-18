
import _external
import _internal

import os
dir = os.path.abspath(os.path.dirname(__file__))

# get files list in current directory and import them to make each library available
files = os.listdir(dir)
modules = [ file[:-3] for file in files if file.endswith(".py") and not file.startswith('_') ]
for module in modules:
	mod = __import__('sconsProject.autoconf.'+module, fromlist=['sconsProject', 'autoconf'])
	globals()[module] = getattr(mod, module)

