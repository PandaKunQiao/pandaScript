import maya.cmds as cmds

def connectMult(driverAttr, drivenAttr):
	nodeLs = cmds.ls(selection = True)
	driverNum = len(nodeLs)/2
	drivenNum = driverNum
	driverLs = nodeLs[:driverNum]
	drivenLs = nodeLs[driverNum:]
	for i in xrange(driverNum):
		cmds.connectAttr(driverLs[i]+driverAttr, drivenLs[i]+drivenAttr, force = True)
	print "success"

def connectOne(driverAttr, drivenAttr):
	nodeLs = cmds.ls(selection = True)
	driver = nodeLs[0]
	drivenLs = nodeLs[1:]
	drivenNum = len(drivenLs)
	for i in xrange(drivenNum):
		cmds.connectAttr(driver+driverAttr, drivenLs[i]+drivenAttr, force = True)
	print "success"