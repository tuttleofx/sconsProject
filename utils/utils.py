'''
Display fonctions.
'''

import atexit
import sys
from colors import colors


# Make the build fail if we pass fail=1 on the command line
#if ARGUMENTS.get('fail', 0):
#	Command('target', 'source', ['/bin/false'])

def bf_to_str(bf):
	'''
    Convert an element of GetBuildFailures() to a string
	in a useful way.
    '''
	import SCons.Errors
	if bf is None: # unknown targets product None in list
		return '(unknown tgt)'
	elif isinstance(bf, SCons.Errors.StopError):
		return str(bf)
	elif bf.node:
		return str(bf.node) + ': ' + bf.errstr
	elif bf.filename:
		return bf.filename + ': ' + bf.errstr
	return 'unknown failure: ' + bf.errstr

def build_status():
	'''Convert the build status to a 2-tuple, (status, msg).'''
	from SCons.Script import GetBuildFailures
	bf = GetBuildFailures()
	if bf:
		# bf is normally a list of build failures; if an element is None,
		# it's because of a target that scons doesn't know anything about.
		status = 'failed'
		failures_message = "\n".join(["Failed building %s" % bf_to_str(x)
			for x in bf if x is not None])
	else:
		# if bf is None, the build completed successfully.
		status = 'ok'
		failures_message = ''
	return (status, failures_message)

def display_build_status(removedFromDefaultTargets):
	'''
    Display the build status.  Called by atexit.
	Here you could do all kinds of complicated things.
    '''
	status, failures_message = build_status()
	if status == 'failed':
		print colors['fail']
		print ">>>"
		print ">>> build failed"
		print ">>>" + colors['clear']
	elif status == 'ok':
		print colors['success']
		print ">>>"
		print ">>> build succeeded"
		print ">>>" + colors['clear']
		if removedFromDefaultTargets:
			print "\nSome targets have been removed from default targets, due to missing dependencies:"
			for k, v in removedFromDefaultTargets.iteritems():
				print " * '%s': %s" % (k, str(v))
			print "\nSee 'config.log' to see the configure errors."
	print failures_message



def clear_atexit_excepthook(exctype, value, traceback):
    '''
    When an exception is raised, don't print build status... and print a
    message to explain that there is an error in a SCons file.
    '''
    atexit._exithandlers[:] = []
    sys.__excepthook__(exctype, value, traceback)
    print colors['fail']
    print ">>>"
    print ">>> scons error"
    print ">>>" + colors['clear']

# this don't work...
sys.excepthook = clear_atexit_excepthook

