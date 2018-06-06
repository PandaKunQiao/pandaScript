#cumstom menu by Fred Qiao
import maya.cmds as cmds
from functools import partial
import zero_out as zo
import colorchanging as cc
import fkik as fi
import ribbonarm as rb
import connection as cn

#    Create a window with two menu bar layouts.
#


def pandaMenu():
	pandaWindow = cmds.window("PandaM Menu Version 0.1")
	cmds.columnLayout( adjustableColumn=True )

	#    Create first menu bar layout.
	#
	menuBarLayout = cmds.menuBarLayout()
	cmds.menu( label='Rigging' )
	mi_zero_out = cmds.menuItem(label='Zero Out', command = partial(zo.win))
	cmds.menuItem( label='Color Controls', command = partial(cc.win))
	cmds.menuItem( label='FK IK Switch', command = partial(fi.win) )
	cmds.menuItem( label="Ribbon Creator", command = partial(rb.win))
	cmds.menuItem( label="Connection Tool", command = partial(cn.init_win))

	cmds.menu( label='Help', helpMenu=True )
	cmds.menuItem( label='About...' )

	cmds.setParent( '..' )

	cmds.separator( height=10, style='none' )

	#    Create a second menu bar layout.
	#
	cmds.menuBarLayout()
	cmds.menu( label='Edit' )
	cmds.menuItem( label='Cut' )
	cmds.menuItem( label='Copy' )
	cmds.menuItem( label='Paste' )

	cmds.menu( label='View' )
	cmds.menuItem( label='Fonts...' )
	cmds.menuItem( label='Colors...' )

	cmds.columnLayout()
	cmds.text( label='Add some controls here.' )
	cmds.setParent( '..' )
	cmds.setParent( '..' )
	cmds.showWindow( pandaWindow )
