from _external import *
from pthread import *

wxwidgets = LibWithHeaderChecker( 
			['wx_gtk2u_xrc-2.6','wx_gtk2u_qa-2.6','wx_gtk2u_html-2.6', 'wx_gtk2u_adv-2.6', 'wx_gtk2u_core-2.6', 'wx_baseu_xml-2.6', 'wx_baseu_net-2.6',  'wx_baseu-2.6' ],
			'wx/wx.h',
			'c++',
			name='wxwidgets',
			defines=['GTK_NO_CHECK_CASTS', '__WXGTK__' ,'_FILE_OFFSET_BITS=64' ,'_LARGE_FILES',  'NO_GCC_PRAGMA'],
			dependencies=[ pthread] )

