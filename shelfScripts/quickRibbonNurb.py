import maya.cmds as cmds

def createRibbon(jntLs):
	totalDist = 0
	cmds.select(clear = True)
	jntNum = len(jntLs)
	faceNum = jntNum * 5
	offSetFace = 5
	for i in xrange(len(jntLs)):
		if i != 0:
			totalDist += cmds.getAttr(jntLs[i] + ".translateX")
	length = totalDist / (faceNum - 5) * faceNum
	plane = cmds.nurbsPlane(axis = [0, 1, 0], constructionHistory = True, degree = 3, lengthRatio = length, pivot = [0, 0, 0], patchesU = 1, patchesV = faceNum)[0]
	cmds.setAttr(plane + ".translateX", length/2)
	cmds.setAttr(plane + ".rotateX", 90)
	cmds.setAttr(plane + ".rotateZ", -90)
	cmds.makeIdentity(plane, apply = True, translate = True, rotate = True)
	cmds.xform(plane, pivots = [offSetFace/2.0 * length/faceNum, 0, 0])
	cons = cmds.parentConstraint(jntLs[0], plane, maintainOffset = False)
	cmds.delete(cons)
createRibbon(cmds.ls(selection = True))