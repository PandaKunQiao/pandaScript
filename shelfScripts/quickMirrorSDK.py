import maya.cmds as cmds
import string

# How to use:
# First, select controls whose poses need to be mirrored 
# (the transform node right parent the shape node)
# Then, run the code

def getRefList(childNode):
	rstList = []
	while childNode[0:4] != "ref_":
		rstList += [childNode]
		childNode = cmds.listRelatives(childNode, parent = True)[0]
	rstList += [childNode]
	return rstList


def mirrorSDK(transLs):
	for node in transLs:
		refList = getRefList(node)[1:-1]
		for ref in refList:
			rX = cmds.getAttr(ref+".rotateX")
			rY = cmds.getAttr(ref+".rotateY")
			rZ = cmds.getAttr(ref+".rotateZ")
			if "_l_" in ref:
				mirroredRef = string.replace(ref, "_l_", "_r_")
			else:
				mirroredRef = string.replace(ref, "_r_", "_l_")
			cmds.setAttr(mirroredRef + ".rotateX", rX)
			cmds.setAttr(mirroredRef + ".rotateY", rY)
			cmds.setAttr(mirroredRef + ".rotateZ", rZ)

mirrorSDK(cmds.ls(selection = True, flatten = True))