import maya.cmds as cmds
def quickConnect(driverName, drivenName):
	tempNode = cmds.createNode("multMatrix")
	cmds.connectAttr(drivenName + ".worldMatrix[0]", tempNode + ".matrixIn[0]")
	cmds.connectAttr(driverName + ".worldInverseMatrix[0]", tempNode + ".matrixIn[1]")
	print cmds.dgeval(tempNode + ".matrixSum")
	offsetVal = cmds.getAttr(tempNode + ".matrixSum")
	print driverName
	print drivenName
	print offsetVal
	cmds.setAttr(multMatrix + ".matrixIn[0]", offsetVal, type = "matrix")
	cmds.delete(tempNode)
	multMatrix = cmds.createNode("multMatrix", name = "parentConstraint_" + drivenName + "_mMatrix")
	decomposeMatrix = cmds.createNode("decomposeMatrix", name = "parentConstraint_" + driverName + "_dMatrix")
	# cmds.connectAttr(driverName + ".scale", composeMatrix + ".inputScale", force = True)
	cmds.connectAttr(driverName + ".worldMatrix[0]", multMatrix + ".matrixIn[1]")
	cmds.connectAttr(drivenName + ".parentInverseMatrix[0]", multMatrix + ".matrixIn[2]")
	cmds.connectAttr(multMatrix + ".matrixSum", decomposeMatrix + ".inputMatrix")
	cmds.connectAttr(decomposeMatrix + ".outputTranslate", drivenName + ".translate", force = True)
	cmds.connectAttr(decomposeMatrix + ".outputRotate", drivenName + ".rotate", force = True)

	

quickConnect(cmds.ls(selection = True)[0], cmds.ls(selection = True)[1])