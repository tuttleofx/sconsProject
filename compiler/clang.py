import os
import sys
import gcc

name = 'clang'
ccBin = 'clang'
cxxBin = 'clang++'
linkBin = ccBin
linkxxBin = cxxBin

def version( bin = 'clang' ):
	import subprocess
	try:
		return subprocess.Popen( [bin, CC['version']], stdout=subprocess.PIPE, stderr=subprocess.PIPE ).communicate()[0].strip()
	except:
		return 'unknown'

ccVersionStr = version()
ccVersion = [0,0,0]
if ccVersionStr != 'unknown':
	ccVersion = [int(i) for i in ccVersionStr.split('.')]

# by default, same interface than gcc
CC = gcc.CC

