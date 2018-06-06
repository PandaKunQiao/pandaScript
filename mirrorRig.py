import maya.cmds as cmds
from functools import partial
import maya.mel as mel
import math
import string
import copy
import numpy as np

def getTop(Node):
	result = Node
	for i in xrange(100):
		resultList = cmds.listRelatives(result, parent = True)
		if resultList == None:
			return result
		else:
			result = resultList[0]
	return None

def replaceNameList(origTarget, newTarget, L):
	result = []
	for name in L:
		result += [string.replace(name, origTarget, newTarget)]
	return result

# mirror the switch controls
# input: original and new direction, the input control list
# side effect: create mirrored controls
# output:a list of mirrored controls
def mirrorFKCtrls(inputDirection, outputDirection, inputCtrlList):
	cmds.select([])
	tempParentLocator = cmds.spaceLocator()[0]
	cmds.select([])
	topNode = getTop(inputCtrlList[0])
	cmds.parent(topNode, tempParentLocator)
	tempCopyParentLocator = cmds.duplicate(tempParentLocator)[0]
	cmds.select([])
	cmds.xform(tempCopyParentLocator, scale = [-1, 1, 1])
	cmds.select(tempCopyParentLocator)
	if inputDirection == "l":
		mel.eval('searchReplaceNames "_l_" "_r_" "hierarchy";')
	else:
		mel.eval('searchReplaceNames "_r_" "_l_" "hierarchy";')
	mirroredTopNode = cmds.listRelatives(tempCopyParentLocator,
										 children = True, 
										 type = "transform")[0]
	cmds.parent(mirroredTopNode, world = True)
	cmds.parent(topNode, world = True)
	cmds.delete([tempParentLocator, tempCopyParentLocator])
	return replaceNameList("_" + inputDirection + "_", 
						   "_" + outputDirection + "_", 
						   inputCtrlList)
# parent constraint jnt to ctrl in order
def parentFKCtrls(ctrlList, jntList):
	for index in xrange(len(ctrlList)):
		ctrl = ctrlList[index]
		jnt = jntList[index]
		cmds.parentConstraint(ctrl, jnt)

# mirror the switch controls
# input: original and new direction, the input control list
# side effect: create mirrored controls
# output:a list of mirrored controls
def mirrorIKCtrls(inputDirection, outputDirection, inputCtrlList):

	# select stuff
	cmds.select([])
	tempParentLocator = cmds.spaceLocator()[0]
	cmds.select([])
	topNodeList = []

	# parent ctrls to the locator
	for ctrl in inputCtrlList:
		topNode = getTop(ctrl)
		topNodeList += [topNode]
		cmds.parent(topNode, tempParentLocator)
	tempCopyParentLocator = cmds.duplicate(tempParentLocator)[0]
	cmds.select([])
	cmds.xform(tempCopyParentLocator, scale = [-1, 1, 1])
	cmds.select(tempCopyParentLocator)
	if inputDirection == "l":
		mel.eval('searchReplaceNames "_l_" "_r_" "hierarchy";')
	else:
		mel.eval('searchReplaceNames "_r_" "_l_" "hierarchy";')
	mirroredTopNodeList = cmds.listRelatives(tempCopyParentLocator,
										 	children = True, 
										 	type = "transform")

	# unparent mirrored reference node and original reference node back to world
	for mirroredTopNode in mirroredTopNodeList:
		cmds.parent(mirroredTopNode, world = True)
	for topNode in topNodeList:
		cmds.parent(topNode, world = True)

	# delete everything
	cmds.delete([tempParentLocator, tempCopyParentLocator])
	return replaceNameList("_" + inputDirection + "_", 
						   "_" + outputDirection + "_", 
						   inputCtrlList)


# given controls, joints, ikhandle,
# side effect: rig it
# output: none
def rigIKCtrls(ctrlList, jntList, mirroredHandle):
	cmds.poleVectorConstraint(ctrlList[0], mirroredHandle)
	cmds.pointConstraint(ctrlList[1], mirroredHandle)


# mirror the switch controls
# input: original and new direction, the input control list
# side effect: create mirrored controls
# output:a list of mirrored controls
def mirrorSwitchCtrls(inputDirection, outputDirection, inputCtrlList):
	cmds.select([])
	tempParentLocator = cmds.spaceLocator()[0]
	cmds.select([])
	topNode = getTop(inputCtrlList[0])
	cmds.parent(topNode, tempParentLocator)
	tempCopyParentLocator = cmds.duplicate(tempParentLocator)[0]
	cmds.select([])
	cmds.xform(tempCopyParentLocator, scale = [-1, 1, 1])
	cmds.select(tempCopyParentLocator)
	if inputDirection == "l":
		mel.eval('searchReplaceNames "_l_" "_r_" "hierarchy";')
	else:
		mel.eval('searchReplaceNames "_r_" "_l_" "hierarchy";')
	mirroredTopNode = cmds.listRelatives(tempCopyParentLocator,
										 children = True, 
										 type = "transform")[0]
	cmds.parent(mirroredTopNode, world = True)
	cmds.parent(topNode, world = True)
	cmds.delete([tempParentLocator, tempCopyParentLocator])
	return replaceNameList("_" + inputDirection + "_", 
						   "_" + outputDirection + "_", 
						   inputCtrlList)



# input: the node type that is looked for, list to find
# output: either none or node that has type nodetype
def findTypeInList(nodeType, L):
	for node in L:
		if cmds.nodeType(node) == nodeType:
			return node
	return None


# return mirrored ikhandle if the arm is using IK, None if not
def mirrorJntWrapper(rootInputJnt, inputDirection, outputDirection, 
					inputJntList, outputJntList):
	print "_" + inputDirection + "_"
	print "_" + outputDirection + "_"
	rootOutputJntList = cmds.mirrorJoint(rootInputJnt, mirrorBehavior = True, 
						mirrorYZ = True, 
						searchReplace = ("_" + inputDirection + "_", 
										 "_" + outputDirection + "_"))

	outputJntList += replaceNameList("_" + inputDirection + "_", 
									 "_" + outputDirection + "_",
									 inputJntList)
	if cmds.listConnections(findTypeInList("ikEffector", rootOutputJntList), 
													type = "ikHandle") == None:
		return None
	else:
		return cmds.listConnections(findTypeInList("ikEffector", 
													rootOutputJntList), 
													type = "ikHandle")[0]


def get_main_name(name, prefix):
	main_name = name[len(prefix):]
	print "main name is" + main_name
	return main_name

def add_prefix(name, prefix):
	new_name = prefix + name
	print "new name is " + new_name
	return new_name

def select_node(node_name, *args):
	cmds.select(node_name, replace = True)

def get_weightAttr_name(constraint_name, joint_name, suffix):
	return constraint_name + "." + joint_name + suffix

#helper to zero out the control, return a list that contains all the new 
# reference nodes
def createSwitch(control_name, attr_name, joint_list):
	bind_prefix = "bn_"
	ik_prefix = "ik_"
	fk_prefix = "fk_"
	reverse_name = "rev_l_arm"
	list_objects = joint_list
	num_objects = len(list_objects)

	#reverse node
	reverse_node = cmds.createNode("reverse", name = reverse_name)

	#the returned list
	list_new_nodes = []
	ik_joint_chain = []
	fk_joint_chain = []
	parent_constraint_chain = []
	#go through all the selected nodes
	for i in xrange(num_objects):

		ith_bind_name = list_objects[i]
		ith_joint_name = get_main_name(ith_bind_name, bind_prefix)
		ith_ik_name = add_prefix(ith_joint_name, ik_prefix)
		ith_fk_name = add_prefix(ith_joint_name, fk_prefix)
		ith_ik_joint = cmds.duplicate(ith_bind_name, parentOnly = True, 
										name = ith_ik_name)
		ith_fk_joint = cmds.duplicate(ith_bind_name, parentOnly = True, 
										name = ith_fk_name)
		ik_joint_chain += [ith_ik_joint]
		fk_joint_chain += [ith_fk_joint]
		ith_parentConstraint = cmds.parentConstraint(ith_ik_joint, ith_fk_joint, 
													 ith_bind_name)

		#connect reverse node to the fk weight
		cmds.connectAttr(reverse_node+".outputX", 
						 get_weightAttr_name(ith_parentConstraint[0], 
						 					 ith_fk_joint[0], "W1"))
		cmds.connectAttr(control_name + "." + attr_name, 
						 get_weightAttr_name(ith_parentConstraint[0], 
						 				 	 ith_ik_joint[0], "W0"))

	for i in xrange(num_objects-1, 0, -1):
		cmds.parent(ik_joint_chain[i], ik_joint_chain[i-1])
		cmds.parent(fk_joint_chain[i], fk_joint_chain[i-1])

	#create IK handle
	print str(ik_joint_chain[-1])
	handle = cmds.ikHandle(startJoint = ik_joint_chain[0][0], 
				endEffector = ik_joint_chain[-1][0], solver = "ikRPsolver")[0]
	cmds.connectAttr(control_name + "." + attr_name, reverse_node+".inputX")
	return [handle, ik_joint_chain, fk_joint_chain]



# function to mirror the joint, get all input and will fill in the out put,
# outpu: nothing
def mirror(fakeInput, 
		   inputJntList, outputJntList,
		   inputFKJntList, outputFKJntList, inputIKJntList, outputIKJntList,
		   inputIKCtrlList, inputFKCtrlList, inputSwitchCtrlList,
		   outputIKCtrlList, outputFKCtrlList, outputSwitchCtrlList,
		   inputDirectionList, outputDirectionList,
		   ctrlTypeList):
	if inputDirectionList[0] == "r":
		outputDirectionList += "l"
	else:
		outputDirectionList += "r"
	inputDirection = inputDirectionList[0]
	outputDirection = outputDirectionList[0]
	if ("FK" in ctrlTypeList[0] and "IK" in ctrlTypeList[0]):
		ctrlType = "FKIK"
	elif ("FK" in ctrlTypeList[0]):
		ctrlType = "FK"
	else:
		ctrlType = "IK"
	ctrlType = ctrlTypeList[0]
	rootInputJnt = inputJntList[0]
	mirroredHandle = mirrorJntWrapper(rootInputJnt, inputDirection, 
								  outputDirection, inputJntList, outputJntList)
	

	if ctrlType == "FK":
		outputFKCtrlList += mirrorFKCtrls(inputDirection, outputDirection, 
										  inputFKCtrlList)
		parentFKCtrls(outputFKCtrlList, outputJntList)
	elif ctrlType == "IK":
		outputIKCtrlList += mirrorIKCtrls(inputDirection, outputDirection,
										  inputIKCtrlList)
		rigIKCtrls(outputIKCtrlList, outputJntList, mirroredHandle)
	else:
		outputFKCtrlList += mirrorFKCtrls(inputDirection, outputDirection, 
										  inputFKCtrlList)
		outputIKCtrlList += mirrorIKCtrls(inputDirection, outputDirection,
										  inputIKCtrlList)
		outputSwitchCtrlList += mirrorSwitchCtrls(inputDirection, 
												  outputDirection, 
												  inputSwitchCtrlList)
		[handle, IKJntList, FKJntList] = createSwitch(outputSwitchCtrlList[0], 
														"ik_arm", outputJntList)
		parentFKCtrls(outputFKCtrlList, FKJntList)
		rigIKCtrls(outputIKCtrlList, IKJntList, handle)
		outputFKJntList += FKJntList
		outputIKJntList += IKJntList



# tests
# test fk
# mirror(['bn_autoArm_l_1', 'bn_autoArm_l_2', 'bn_autoArm_l_3'], [], 
# 	   ['ctrl_fk_l_shoulder', 'ctrl_fk_l_elbow', 'ctrl_fk_l_wrist'], [],
# 	   ["l"], [], ["FK"])

# test ik
# mirror(['bn_autoArm_l_1', 'bn_autoArm_l_2', 'bn_autoArm_l_3'], [],
# 		[], [], [], [],
# 	   ['ctrl_ik_l_elbow', 'ctrl_ik_l_wrist'], [], [],
# 	   [], [], [],
# 	   ["l"], [], ["IK"])
# test fkik
# mirror(['bn_autoArm_l_1', 'bn_autoArm_l_2', 'bn_autoArm_l_3'], [],
# 		['fk_autoArm_l_1', 'fk_autoArm_l_2', 'fk_autoArm_l_3'], [], ['ik_autoArm_l_1', 'ik_autoArm_l_2', 'ik_autoArm_l_3'], [],
# 	   ['ctrl_ik_l_elbow', 'ctrl_ik_l_wrist'], ['ctrl_fk_l_shoulder', 'ctrl_fk_l_elbow', 'ctrl_fk_l_wrist'], ["ctrl_l_arm_switch"],
# 	   [], [], [],
# 	   ["l"], [], [""])
# mirrorFKCtrls("l", ['ctrl_fk_l_shoulder', 'ctrl_fk_l__elbow', 'ctrl_fk_l_wrist'])