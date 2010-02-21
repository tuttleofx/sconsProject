
black  = '0'
red    = '1'
green  = '2'
yellow = '3'
blue   = '4'
violet = '5'
cyan   = '6'
white  = '7'

#text       = '3'
text       = '9'
background = '4'
bold       = ';1m'
normal     = 'm'
color      = '\033['
# or \x1B[ or \E[
# code ASCII 27 => ESC


#-------------------------------------------------------------------------------
# colors
#-------------------------------------------------------------------------------
colors = {}

colors['clear']  = color + '0m'

colors['green']  = color + text + green  + normal
colors['cyan']   = color + text + cyan   + normal
colors['blue']   = color + text + blue   + normal
colors['blueB']  = color + text + blue   + bold
colors['brown']  = color + text + yellow + normal
colors['yellow'] = color + text + yellow + bold
colors['red']    = color + text + red    + normal
colors['redB']   = color + text + red    + bold
colors['violet'] = color + text + violet + normal

#-------------------------------------------------------------------------------
# display
#-------------------------------------------------------------------------------

colors['autoconf'] = colors['blue']
colors['header']   = colors['violet']
colors['title']    = colors['red']

colors['info']     = colors['brown']
colors['success']  = colors['green']
colors['warning']  = colors['redB']
colors['fail']     = colors['red']
colors['error']    = color + background + red + ';' + text + white + normal




# to disable colors :
# colors = {}
# for i in colors:
#	i = ''
