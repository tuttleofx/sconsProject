from _external import *

def locateCommand(env, cmd, bindir):
	path = env.WhereIs(cmd, path=bindir)
	if path:
		return path
	return cmd

class CudaChecker(LibWithHeaderChecker):
	'''
	Cuda checker
	'''

	def __init__( self,
				  libs = ['cuda','cudart','cutil'],
				  header = ['cuda.h'],
				  language = 'c',
				  defines = [] ):
		LibWithHeaderChecker.__init__(self, libs, header, language, name='cuda', defines=defines )

	def initOptions(self, project, opts):
		LibWithHeaderChecker.initOptions(self, project, opts)
		opts.Add( 'bindir_'+self.name,   'Base directory for '+self.name, '${_join_if_basedir_not_empty( dir_'+self.name+ ', "bin" )}' )
		return True

	def configure(self, project, env):
		#bindir = '$bindir_'+self.name
		#nvcc = locateCommand(env, 'nvcc', bindir)
		#env.SetDefault(
		#		NVCC = '${_whereIs( "nvccaa", bindir_cuda )}',
		#	)
		#print 'CudaChecker.configure'
		#env.PrependENVPath( 'PATH', '$bindir_'+self.name )
		env.PrependENVPath( 'PATH', env['bindir_'+self.name] )
		return LibWithHeaderChecker.configure(self, project, env)

#cuda = LibWithHeaderChecker( ['cuda','cudart'], 'cuda.h', 'c', name='cuda')
cuda = CudaChecker()

