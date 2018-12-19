import maya.cmds as cmds
def makeAimConstraint(parent, child, worldUpObj, aimVector, upVector, worldUpVector):
	midName = parent + child + "_aim_"

	# create parent decompose matrix and connect
	parentDM = cmds.createNode("decomposeMatrix", name = parent + midName + "decomposeMatrix")
	cmds.connectAttr(parent + ".worldMatrix[0]", parentDM + ".inputMatrix")

	# create a duplicate of child to avoid cycles
	childTrans = cmds.createNode("transform", name = child + midName + "srt")
	cmds.connectAttr(child + ".translate", childTrans + ".translate")
	cmds.parent(childTrans, cmds.listRelatives(child, parent = True)[0])

	# create child decompose matrix and connect
	childDM = cmds.createNode("decomposeMatrix", name = child + midName + "decomposeMatrix")
	cmds.connectAttr(childTrans + ".worldMatrix[0]", childDM + ".inputMatrix")

	# create the aim vector node and connect
	aimMinus = cmds.createNode("plusMinusAverage", name = midName + "aimVector")
	cmds.connectAttr(parentDM + ".outputTranslate", aimMinus + ".input3D[0]")
	cmds.connectAttr(childDM + ".outputTranslate", aimMinus + ".input3D[1]")
	cmds.setAttr(aimMinus + ".operation", 2)

	# create the xaxis, connect and normalize
	# this set up is for aimVector = [1, 0, 0], upVector = [0, 1, 0]
	xAxis = cmds.createNode("vectorProduct", name = midName + "xVector")
	cmds.connectAttr(aimMinus + ".output3D", xAxis + ".input1")
	cmds.setAttr(xAxis + ".normalizeOutput", 1)
	cmds.setAttr(xAxis + ".operation", 0)

	# create world up vector, nomalize and connect
	worldUpVec = cmds.createNode("vectorProduct"， name = midName + "upVector")
	cmds.connectAttr(worldUpObj + ".worldMatrix[0]", worldUpVec + ".matrix")
	cmds.setAttr(worldUpVec + ".operation", 3)
	cmds.setAttr(worldUpVec + ".input1X", worldUpVector[0])
	cmds.setAttr(worldUpVec + ".input1Y", worldUpVector[1])
	cmds.setAttr(worldUpVec + ".input1Z", worldUpVector[2])
	cmds.setAttr(worldUpVec + ".normalizeOutput", 1)

	# create zaxis, connect and normalize
	# using world up vector to find z axis
	zAxis = cmds.createNode("vectorProduct", name = midName + "zVector")
	cmds.connectAttr(worldUpVec + ".output", zAxis + ".input1")
	cmds.connectAttr(aimMinus + ".output3D", zAxis + ".input2")
	cmds.setAttr(zAxis + ".normalizeOutput", 1)
	cmds.setAttr(zAxis + ".operation", 2)

	# create yaxis, connect and normalize
	yAxis = cmds.createNode("vectorProduct", name = midName + "yVector")
	cmds.connectAttr(zAxis + ".output", yAxis + ".input2")
	cmds.connectAttr(aimMinus + ".output3D", yAxis + ".input1")
	cmds.setAttr(yAxis + ".normalizeOutput", 1)
	cmds.setAttr(yAxis + ".operation", 2)


	# create matrices to adjust aim vectors
	# the input matrix
	changeDirectionMatrix = cmds.createNode("fourByFourMatrix", name = midName + "vectorOffsetMatrix")
	cmds.setAttr(changeDirectionMatrix + ".in00", aimVector[0])
	cmds.setAttr(changeDirectionMatrix + ".in01", aimVector[1])
	cmds.setAttr(changeDirectionMatrix + ".in02", aimVector[2])
	cmds.setAttr(changeDirectionMatrix + ".in10", upVector[0])
	cmds.setAttr(changeDirectionMatrix + ".in11", upVector[1])
	cmds.setAttr(changeDirectionMatrix + ".in12", upVector[2])
	tempZ = cmds.createNode("vectorProduct")
	cmds.setAttr(tempZ + ".operation", 2)
	cmds.setAttr(tempZ + ".normalizeOutput", 1)
	cmds.setAttr(tempZ + ".input1.input1X", upVector[0])
	cmds.setAttr(tempZ + ".input1.input1Y", upVector[1])
	cmds.setAttr(tempZ + ".input1.input1Z", upVector[2])
	cmds.setAttr(tempZ + ".input2.input2X", aimVector[0])
	cmds.setAttr(tempZ + ".input2.input2Y", aimVector[1])
	cmds.setAttr(tempZ + ".input2.input2Z", aimVector[2])
	matrixZX = cmds.getAttr(tempZ + ".output.outputX")
	matrixZY = cmds.getAttr(tempZ + ".output.outputY")
	matrixZZ = cmds.getAttr(tempZ + ".output.outputZ")
	cmds.setAttr(changeDirectionMatrix + ".in20", matrixZX)
	cmds.setAttr(changeDirectionMatrix + ".in21", matrixZY)
	cmds.setAttr(changeDirectionMatrix + ".in22", matrixZZ)

	# create the inverse matrix
	changeDirectionInverse = cmds.createNode("inverseMatrix", name = midName + "vectorInverseMatrix")
	changeMatrixValue = cmds.getAttr(changeDirectionMatrix + ".output")
	cmds.setAttr(changeDirectionInverse + ".inputMatrix", changeMatrixValue, type = "matrix")


	# create the world matrix before offset, then connect
	resultWorldMatrix = cmds.createNode("fourByFourMatrix", name = midName + "worldMatrix")
	cmds.connectAttr(xAxis + ".outputX", resultWorldMatrix + ".in00")
	cmds.connectAttr(xAxis + ".outputY", resultWorldMatrix + ".in01")
	cmds.connectAttr(xAxis + ".outputZ", resultWorldMatrix + ".in02")
	cmds.connectAttr(yAxis + ".outputX", resultWorldMatrix + ".in10")
	cmds.connectAttr(yAxis + ".outputY", resultWorldMatrix + ".in11")
	cmds.connectAttr(yAxis + ".outputZ", resultWorldMatrix + ".in12")
	cmds.connectAttr(zAxis + ".outputX", resultWorldMatrix + ".in20")
	cmds.connectAttr(zAxis + ".outputY", resultWorldMatrix + ".in21")
	cmds.connectAttr(zAxis + ".outputZ", resultWorldMatrix + ".in22")


	# create the final matrix
	finalMult = cmds.createNode("multMatrix", name = midName + "offsetMatrix")	
	cmds.connectAttr(resultWorldMatrix + ".output", finalMult + ".matrixIn[1]")
	cmds.connectAttr(changeDirectionInverse + ".outputMatrix", finalMult + ".matrixIn[0]")
	finalDecompose = cmds.createNode("decomposeMatrix", name = midName + "target_decomposeMatrix")
	

	#calculate the offset and do the final sortup
	tempInverse = cmds.createNode("inverseMatrix")
	cmds.connectAttr(finalMult + ".matrixSum", tempInverse + ".inputMatrix")
	tempMult = cmds.createNode("multMatrix")
	cmds.connectAttr(child + ".worldMatrix[0]", tempMult + ".matrixIn[0]")
	cmds.connectAttr(tempInverse + ".outputMatrix", tempMult + ".matrixIn[1]")
	offset = cmds.getAttr(tempMult + ".matrixSum")
	cmds.disconnectAttr(resultWorldMatrix + ".output", finalMult + ".matrixIn[1]")
	cmds.disconnectAttr(changeDirectionInverse + ".outputMatrix", finalMult + ".matrixIn[0]")
	cmds.connectAttr(resultWorldMatrix + ".output", finalMult + ".matrixIn[2]")
	cmds.connectAttr(changeDirectionInverse + ".outputMatrix", finalMult + ".matrixIn[1]")
	cmds.setAttr(finalMult + ".matrixIn[0]", offset, type = "matrix")

	# do the final connection in world space
	cmds.connectAttr(finalMult + ".matrixSum", finalDecompose + ".inputMatrix")
	cmds.connectAttr(child + ".parentInverseMatrix[0]", finalMult + ".matrixIn[3]")
	cmds.connectAttr(finalDecompose + ".outputRotate", child + ".rotate")
	#cmds.delete(tempInverse)
	#cmds.delete(tempMult)


def replaceAimConstraint(aimConstraintNode):
	aimVector = cmds.aimConstraint(aimConstraintNode, query = True, aimVector = True)
	upVector = cmds.aimConstraint(aimConstraintNode, query = True, upVector = True)
	worldUpVector = cmds.aimConstraint(aimConstraintNode, query = True, worldUpVector = True)
	worldUpObj = cmds.aimConstraint(aimConstraintNode, query = True, worldUpObject = True)[0]
	parent = cmds.aimConstraint(aimConstraintNode, query = True, targetList = True)[0]
	child = cmds.listRelatives(aimConstraintNode, parent = True)[0]
	cmds.delete(aimConstraintNode)
	# the case that it is a joint
	cmds.setAttr(child + ".jointOrientX", 0)
	cmds.setAttr(child + ".jointOrientY", 0)
	cmds.setAttr(child + ".jointOrientZ", 0)
	makeAimConstraint(parent, child, worldUpObj, aimVector, upVector, worldUpVector)


def replaceAllAimconstraintList(aimList):
	for aim in aimList:
		replaceAimConstraint(aim)
	print aim + " aimFinished"

def replaceSelection():
	replaceAllAimconstraintList(cmds.ls(selection = True))