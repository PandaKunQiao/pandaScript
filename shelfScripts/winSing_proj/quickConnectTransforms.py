#cumstom menu by Fred Qiao
import maya.cmds as cmds
from functools import partial


##################################################################################
#							Main Procedure Helpers							     #
##################################################################################
def quickConnectLs():
	objLs = cmds.ls(selection = True)
	pairLen = len(objLs)/2
	print pairLen
	for i in xrange(pairLen):
		driverName = objLs[i]
		drivenName = objLs[pairLen+i]
		print driverName + " " + drivenName
		cmds.connectAttr(driverName + ".translate", drivenName + ".translate", force = True)
		cmds.connectAttr(driverName + ".rotate", drivenName + ".rotate", force = True)
		cmds.connectAttr(driverName + ".scale", drivenName + ".scale", force = True)

quickConnectLs()