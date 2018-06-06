#cumstom menu by Fred Qiao
import maya.cmds as cmds
from functools import partial


##################################################################################
#							Main Procedure Helpers							     #
##################################################################################
def quickConnect():
	objLs = cmds.ls(selection = True)
	driverName = objLs[0]
	drivenName = objLs[1]
	cmds.connectAttr(driverName + ".translate", drivenName + ".translate", force = True)
	cmds.connectAttr(driverName + ".rotate", drivenName + ".rotate", force = True)
	cmds.connectAttr(driverName + ".scale", drivenName + ".scale", force = True)

quickConnect()