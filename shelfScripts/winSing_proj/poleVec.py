import maya.OpenMaya as om
import maya.cmds as cmds
selectLs = cmds.ls(selection = True)
objLs = cmds.ls(selectLs[3], selectLs[0], selectLs[4])
jntList = cmds.ls(selectLs[0], selectLs[1], selectLs[2])
startJnt = jntList[0]
midJnt = jntList[1]
endJnt = jntList[2]
startV = cmds.xform(startJnt, worldSpace = True, translation = True, query = True)
midV = cmds.xform(midJnt, worldSpace = True, translation = True, query = True)
endV = cmds.xform(endJnt, worldSpace = True, translation = True, query = True)
startV = om.MVector(startV[0], startV[1], startV[2])
midV = om.MVector(midV[0], midV[1], midV[2])
endV = om.MVector(endV[0], endV[1], endV[2])


projToV = endV - startV
projFromV = midV - startV

scale = float(projToV * projFromV) / float(projToV.length())
uniToV = projToV.normal()
projV = uniToV * scale
arrowV = (projFromV - projV) * 0.5
finalV = arrowV + midV

zV = projToV ^ projFromV
zV.normalize() 
rotMatrix = [arrowV.x, arrowV.y, arrowV.z, 0,
			 projToV.x, projToV.y, projToV.z, 0,
			 zV.x, zV.y, zV.z, 0,
			 0, 0, 0, 1]
tempMatrix = cmds.createNode("decomposeMatrix")
cmds.setAttr(tempMatrix + ".inputMatrix", rotMatrix, type = "matrix")
poleVec = cmds.spaceLocator()
cmds.xform(poleVec, translation = [finalV.x, finalV.y, finalV.z])
print cmds.getAttr(tempMatrix + ".outputRotate")
cmds.xform(poleVec, rotation = cmds.getAttr(tempMatrix + ".outputRotate")[0])
cmds.delete(tempMatrix)
print rotMatrix

def addPoleVecConstraint(parent, child, ikHandle):
	parentDm = cmds.createNode("decomposeMatrix", name = parent + "_poleVecConstraint_dm")
	childDm = cmds.createNode("decomposeMatrix", name = child + "_poleVecConstraint_dm")
	cmds.connectAttr(parent + ".worldMatrix[0]", parentDm + ".inputMatrix")
	cmds.connectAttr(child + ".worldMatrix[0]", childDm + ".inputMatrix")
	pm = cmds.createNode("plusMinusAverage", name = parent + "_" + child + "_poleVecConstraint_plus")
	cmds.setAttr(pm + ".operation", 2)
	cmds.connectAttr(parentDm + ".outputTranslate", pm + ".input3D[1]")
	cmds.connectAttr(childDm + ".outputTranslate", pm + ".input3D[0]")
	cmds.connectAttr(pm + ".output3D", ikHandle + ".poleVector")

addPoleVecConstraint(objLs[0], objLs[1], objLs[2])