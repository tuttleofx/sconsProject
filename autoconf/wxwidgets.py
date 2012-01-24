from _external import *
from pthread import *

wxwidgets = LibWithHeaderChecker( 
			['wx_gtk2u_xrc-$version_wxwidgets',
			 'wx_gtk2u_qa-$version_wxwidgets',
			 'wx_gtk2u_html-$version_wxwidgets',
			 'wx_gtk2u_adv-$version_wxwidgets',
			 'wx_gtk2u_core-$version_wxwidgets',
			 'wx_baseu_xml-$version_wxwidgets',
			 'wx_baseu_net-$version_wxwidgets',
			 'wx_baseu-$version_wxwidgets' ],
			'wx/wx.h',
			'c++',
			name='wxwidgets',
			version='2.6',
			defines=['GTK_NO_CHECK_CASTS', '__WXGTK__' ,'_FILE_OFFSET_BITS=64' ,'_LARGE_FILES',  'NO_GCC_PRAGMA'],
			dependencies=[ pthread] )

