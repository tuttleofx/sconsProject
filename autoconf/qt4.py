from _external import *
import os

def unique(list) :
        return dict.fromkeys(list).keys()

def subdirs(files):
    dirs = unique(map(os.path.dirname, files))
    dirs.sort()
    return dirs

class Qt4Checker(LibWithHeaderChecker):
    '''
    TODO
    '''

    def __init__(self, modules = [
                'QtCore',
                'QtGui',
                'QtOpenGL',
#                'QtAssistant',
#                'QtScript',
#                'QtDBus',
#                'QtSql',
#                'QtNetwork',
#                'QtSvg',
#                'QtTest',
#                'QtXml',
#                'QtUiTools',
#                'QtDesigner',
#                'QtDesignerComponents',
#                'QtWebKit'
#                'Qt3Support',
                ], uiFiles = [], useLocalIncludes = True ):
        self.name  = 'qt4'
        self.libs = modules
        self.uiFiles = uiFiles
        self.useLocalIncludes = useLocalIncludes
        
    def setModules(self, modules):
        self.libs = modules
        
    def declareUiFiles(self, uiFiles):
        self.uiFiles = uiFiles
        
    def check(self, project, conf):
        conf.env.EnableQt4Modules( self.libs, debug=False )
        result = True
        for mod in self.libs:
            r = self.CheckLibWithHeader( conf, [mod], header=[mod+'/'+mod], language='c++' )
            if not r:
                print 'error: ',mod
            result &= r
        return result
    
    def postconfigure(self, project, env):
        '''
        Cas particulier. Permet d'ajouter des elements a l'environnement apres les checks de toutes les libs.
        '''
        if len(self.uiFiles):
            uis = [env.Uic4( ui ) for ui in self.uiFiles]
            if self.useLocalIncludes:
                env.AppendUnique( CPPPATH=subdirs(self.uiFiles) )
        return True

qt4 = Qt4Checker


