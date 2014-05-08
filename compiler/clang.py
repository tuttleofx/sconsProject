import os
import sys
import gcc

name = 'clang'
ccBin = 'clang'
cxxBin = 'clang++'
arBin = 'ar'
ranlibBin = 'ranlib'
linkBin = ccBin
linkxxBin = cxxBin

def version( bin = 'clang' ):
	import subprocess
	import re
	try:
		versionMsg = subprocess.Popen( [bin, CC['version']], stdout=subprocess.PIPE, stderr=subprocess.PIPE ).communicate()[0].strip()
		versionStr = re.search('.+?clang version (\d(?:.?\d)?).+?', versionMsg).groups()[0]
		# print 'clang version: ', versionStr
		return versionStr
	except:
		return 'unknown'

ccVersionStr = version()
ccVersion = [0,0,0]
if ccVersionStr != 'unknown':
	ccVersion = [int(i) for i in ccVersionStr.split('.')]

# by default, same interface than gcc
CC = dict(gcc.CC)

# "-dumpversion" is a gcc option that still exist on clang for compatibility reasons,
# but it always returns the latest compatible gcc version... which is "4.2.1".
# So use "--version" instead.
CC['version']   = '--version'

# clang doesn't support the GCC debugging symbols flags
CC['debug']   = ['-g'] + CC['nooptimize']

