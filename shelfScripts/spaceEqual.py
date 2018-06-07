import maya.cmds as cmds

def spaceEqual(transLs, direction):
	firstTrans = transLs[0]
	lastTrans = transLs[-1]
	transNum = len(transLs)
	totalDist = 0.0
	for index in xrange(1, transNum):
		totalDist += cmds.getAttr(transLs[index]+ ".translate" + direction)
	eachDist = totalDist/(transNum-1)
	for index in xrange(1, transNum):
		cmds.setAttr(transLs[index] + ".translate" + direction, eachDist)
	return eachDist

spaceEqual(cmds.ls(selection = True), "X")