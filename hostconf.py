
#QTDIR='/usr'
QTDIR='/Developer/SDKs/MacOSX10.6.sdk/Library/Frameworks/'
#______________________________________________________________________________#
#                                   Display                                    #
#______________________________________________________________________________#

color_autoconf = color_blue
color_header   = color_violet
color_title    = color_red
color_info     = color_violet
color_success  = color_green
color_warning  = color_redB
color_fail     = color_red

color_compile  = color_red
color_link     = color_redB
color_install  = color_blue


SHCCCOMSTR    = '''
$color_compile-------------------- Compiling shared object : $TARGET --------------------$color_clear
$SHCCCOM

'''
SHCXXCOMSTR    = '''
$color_compile-------------------- Compiling shared object : $TARGET --------------------$color_clear
$SHCXXCOM

'''
SHLINKCOMSTR  = '''


$color_link==================== Linking shared object : $TARGET ====================$color_clear
$SHLINKCOM


'''
CCCOMSTR      = '''
$color_compile-------------------- Compiling : $TARGET --------------------$color_clear
$CCCOM

'''
CXXCOMSTR      = '''
$color_compile-------------------- Compiling : $TARGET --------------------$color_clear
$CXXCOM

'''
LINKCOMSTR    = '''


$color_link==================== Linking : $TARGET ====================$color_clear
$LINKCOM

'''
ARCOMSTR = '''

$color_link==================== Archiving : $TARGET ====================$color_clear
$ARCOM

'''

INSTALLSTR = '''
$color_install== Install file: $SOURCE as $TARGET ==$color_clear

'''


SWIGCOMSTR    = '''
$color_compile-------------------- SWIG compiling : $TARGET --------------------$color_clear
$SWIGCOM

'''
QT4_MOCFROMCXXCOMSTR = '''
$color_compile-------------------- QT moc (from cpp) compiling : $TARGET --------------------$color_clear
$QT_MOCFROMCXXCOM

'''
QT4_MOCFROMHCOMSTR   = '''
$color_compile-------------------- QT moc (from hpp) compiling : $TARGET --------------------$color_clear
$QT_MOCFROMHCOM

'''
QT4_UICCOMSTR        = '''
$color_compile-------------------- QT uic compiling : $TARGET --------------------$color_clear
$QT_UICCOM

'''