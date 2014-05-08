"""
SConsProject


The sconsproject package proposes a way to easily create the compilation system
of your project with the minimum of information. It's an helper around SCons.

########################################
# Example 1
from sconsProject import SConsProject

project = SConsProject()
Export('project')
Export({'libs':project.libs})

project.begin()
project.SConscript()
project.end()

########################################
# Example 2
# If you have common creation things in your project, create a class for your project which inherite this class.
# So this function is accessible in all SConscript files.
# You can also overload some SConsProject function to cusomize it.
class MyProject( SConsProject ):

        def createCustomPlugins( self, sources=[], libs=[] ):
                \"""
                Create a particular type of plugins from a sources list and a libraries list.
                \"""
                pluginName = self.getName()
                env_local = self.createEnv( libs )
                env_local.AppendUnique( CCFLAGS = self.CC['visibilityhidden'] )
                plugin = env_local.SharedLibrary( target=pluginName, source=sources )
                env_local.InstallAs( self.inOutputBin(), plugin )

project = MyProject(
Export('project')
Export({'libs':project.libs})

project.begin()
project.SConscript()
project.end()
########################################

"""

from project import SConsProject
