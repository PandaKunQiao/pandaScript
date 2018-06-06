import maya.cmds as cmds
from functools import partial
import maya.mel as mel
import math
import string
import copy
import numpy as np
from polyLib import *

def get_main_name(name, prefix):
	main_name = name[len(prefix):]
	print "main name is" + main_name
	return main_name

def add_prefix(name, prefix):
	new_name = prefix + name
	print "new name is " + new_name
	return new_name

def singleButtonWrapper(parent, calledFunction, argList, label):
	if parent == "":
		cmds.rowLayout( numberOfColumns=1, columnAttach=(1, 'both', 15), 
						columnWidth=(1, 550), height = 35 )
		cmds.button(label = label, width = 520, 
			command = partial(calledFunction, argList = argList))
		cmds.setParent("..")
	else:
		cmds.rowLayout( numberOfColumns=1, columnAttach=(1, 'both', 15), 
						columnWidth=(1, 550), height = 35, parent = parent)
		cmds.button(label = label, width = 520,
			command = partial(calledFunction, argList = argList))
		cmds.setParent("..")



def chooseButtonWrapper(parent, label, meshName):
	if parent == "":
		cmds.rowLayout( numberOfColumns = 3, 
						columnAttach = [(1, 'both', 40), 
										(2, "both", 10), 
										(3, "both", 10)], 
						columnWidth=[(1, 300), (2, 120), (3, 120)],
						height = 25)
		cmds.text(label = label)
		cmds.button(label = "select", command = 
			partial(
				chooseMesh, meshName = meshName
			)
		)
		cmds.button(label = "show / hide", command = 
			partial(
				hideShowMesh, meshName = meshName
			)
		)
		cmds.setParent("..")
	else:
		cmds.rowLayout( numberOfColumns = 3, 
						columnAttach = [(1, 'both', 40), 
										(2, "both", 10), 
										(3, "both", 10)], 
						columnWidth=[(1, 300), (2, 120), (3, 120)],
						height = 25, parent = parent)
		cmds.text(label = label)
		cmds.button(label = "select", command = 
			partial(
				chooseMesh, meshName = meshName
			)
		)
		cmds.button(label = "show / hide", command = 
			partial(
				hideShowMesh, meshName = meshName
			)
		)
		cmds.setParent("..")




##################################################################################
#						 Selected Transformation Nodes Window 					 #
##################################################################################





#helper to show which transform node is selected
def fill_selected_object(joint_container, *args):
	name_window = cmds.window("Selected Joints", 
							   sizeable = True,
							   widthHeight = (300, 800),
							   title = "Selected Joints")
	print "name of the window: "
	print name_window
	list_objects = cmds.ls(selection = True)
	joint_container += list_objects
	cmds.columnLayout(columnAttach=("left", 5))
	for i in xrange(len(list_objects)):
		cmds.rowLayout(numberOfColumns = 1, 
					   columnAttach = [(1, "both", 0)],
					   columnWidth = [(1, 300)],
					   height = 40)
		cmds.text(label = list_objects[i])
		cmds.setParent("..")
	cmds.showWindow(name_window)
	cmds.setParent("..")




##################################################################################
#					       New Transform Reference Nodes   						 #
##################################################################################




#helper to select the input node
def select_node(node_name, *args):
	cmds.select(node_name, replace = True)

#helper to close the window
def close_reverse_window(*args):
	cmds.deleteUI("New_Reverse_Node")

def get_weightAttr_name(constraint_name, joint_name, suffix):
	return constraint_name + "." + joint_name + suffix

#helper to create window that contains new reference nodes and selecting buttons
def select_reverse_window(reverse_node_list):
	name_window = cmds.window("New Reverse Node", 
							   sizeable = True,
							   widthHeight = (300, 300),
							   title = "New Reverse Node")
	cmds.columnLayout(columnAttach=("left", 5))
	#list reverse nodes, usually just one
	for i in xrange(len(reverse_node_list)):
		cmds.rowLayout(numberOfColumns = 2,
					   columnAttach = [1, "both", 0],
					   columnWidth = [(1, 300)],
					   height = 40)
		cmds.text(label = reverse_node_list[i])
		cmds.button(label = "Select", command = partial(select_node, reverse_node_list[i]))
		cmds.setParent("..")
	cmds.rowLayout(numberOfColumns = 1,
				   columnAttach = [1, "both", 0],
				   columnWidth = [(1, 300)],
				   height = 40)
	cmds.button(label = "Close", command = partial(close_reverse_window))
	cmds.setParent("..")
	cmds.showWindow(name_window)
	cmds.setParent("..")




#function that triggered when hit the confirm button
def second_button(tfd_name_list, joint_list, *args):
	if cmds.window("Selected_Joints", exists = True):
		cmds.deleteUI("Selected_Joints")
	reverse_node_list = createSwitch(tfd_name_list, joint_list)
	select_reverse_window(reverse_node_list)




################################################################################
#					       UI layout helpers   						 		   #
################################################################################
# This file is for automatically rigging arms

# user interface


# input: (mesh, empty list)
# side effect: input the empty list with vertices of the mesh
# output: None
def getVertsFromMesh(meshList, vertList):
	del vertList[:]
	objList = meshList 
	for obj in objList:
		cmds.select(obj)
		numVert = cmds.polyEvaluate(vertex = True)
		for i in xrange(numVert):
			vertList += [obj + ".vtx[" + str(i) + "]"]

# put the type list into container
def fillBoxType(item, typeList):
	typeList[0] = item

# change the existedTypeList according to new option menu item
def changeTypeList(item, meshName, existedTypeList):
	index = int(meshName[-1])
	existedTypeList[index] = item

# wrapper to choose mesh
def chooseMesh(fakeInput, meshName):
	cmds.select(meshName)

def hideShowMesh(fakeInput, meshName):
	showHide = cmds.getAttr(meshName + ".visibility")
	if showHide:
		cmds.setAttr(meshName + ".visibility", 0)
	else:
		cmds.setAttr(meshName + ".visibility", 1)


# Part to create joints

def calcAngle(pos1, pos2, localDeleteList, direction = "a"):
	# temp_loc = cmds.spaceLocator("loc_temp_angle")
	new_pos = [pos1[0]+1, pos1[1], pos1[2]]
	a = cmds.spaceLocator()
	cmds.xform(a, translation = new_pos)
	# cmds.xform(temp_loc, translation = new_pos)
	temp_vec_1 = cmds.createNode("plusMinusAverage")
	cmds.setAttr(temp_vec_1 + ".operation", 2)
	cmds.setAttr(temp_vec_1+".input3D[0].input3Dx", new_pos[0])
	cmds.setAttr(temp_vec_1+".input3D[0].input3Dy", new_pos[1])
	cmds.setAttr(temp_vec_1+".input3D[0].input3Dz", new_pos[2])
	cmds.setAttr(temp_vec_1+".input3D[1].input3Dx", pos1[0])
	cmds.setAttr(temp_vec_1+".input3D[1].input3Dy", pos1[1])
	cmds.setAttr(temp_vec_1+".input3D[1].input3Dz", pos1[2])

	temp_vec_2 = cmds.createNode("plusMinusAverage")
	cmds.setAttr(temp_vec_2 + ".operation", 2)
	cmds.setAttr(temp_vec_2+".input3D[0].input3Dx", pos2[0])
	cmds.setAttr(temp_vec_2+".input3D[0].input3Dy", pos2[1])
	cmds.setAttr(temp_vec_2+".input3D[0].input3Dz", pos2[2])
	cmds.setAttr(temp_vec_2+".input3D[1].input3Dx", pos1[0])
	cmds.setAttr(temp_vec_2+".input3D[1].input3Dy", pos1[1])
	cmds.setAttr(temp_vec_2+".input3D[1].input3Dz", pos1[2])

	temp_angle = cmds.createNode("angleBetween")
	cmds.connectAttr(temp_vec_1 + ".output3D", temp_angle + ".vector1")
	cmds.connectAttr(temp_vec_2 + ".output3D", temp_angle + ".vector2")
	print a
	cmds.delete(a)
	localDeleteList += [temp_vec_1, temp_vec_2, temp_angle]
	return cmds.getAttr(temp_angle + ".euler")[0]

# given angle and position and the index, 
# create a shoulder joint and return its name
# name convention: armJnt_temp_
def createJoint(direction, pos, angle, num):
	joint = cmds.joint(name = "bn_autoArm_" + direction + "_" + str(num))
	cmds.select([])
	cmds.xform(joint, translation = pos, rotation = angle)
	return joint


# helper function to create the joint chain
def createJointChain(direction, posShoulder, posElbow, posWrist, 
					 localDeleteList):
	shoulderAngle = calcAngle(posShoulder, posElbow, localDeleteList)

	# create shoulder joint
	shoulderJnt = createJoint(direction, posShoulder, shoulderAngle, 1)

	# create elbow joint, parent it under the shoulder
	elbowJoint = createJoint(direction, posElbow, [0, 0, 0], 2)
	cmds.parent(elbowJoint, shoulderJnt)
	cmds.select([])

	# create wrist joint, parent it under the elbow
	wristJoint = createJoint(direction, posWrist, [0, 0, 0], 3)
	cmds.parent(wristJoint, elbowJoint)
	cmds.select([])

	# temporily orient the joint back to 0 to orient joint
	cmds.xform(shoulderJnt, rotation = [0, 0, 0])
	cmds.select(shoulderJnt)
	cmds.joint(edit = True, orientJoint = "xzy", 
							secondaryAxisOrient = "xup", 
							zeroScaleOrient = True, 
							children = True)
	cmds.setAttr(wristJoint + ".jointOrientX", 0)
	cmds.setAttr(wristJoint + ".jointOrientY", 0)
	cmds.setAttr(wristJoint + ".jointOrientZ", 0)
	cmds.xform(shoulderJnt, rotation = shoulderAngle)
	cmds.makeIdentity(shoulderJnt, apply = True, 
								   rotate = True,
								   translate = True,
								   scale = True,
								   preserveNormals = True,
								   normal = False)
	return [shoulderJnt, elbowJoint, wristJoint]

# input a joint name, create a box at joint position and return its name
def createBoxMeshAtJoint(jnt):
	boxMesh = cmds.polyCube(name = "box_" + jnt)[0]
	cmds.select([])
	trans = cmds.xform(jnt, query = True, worldSpace = True, matrix = True)
	cmds.xform(boxMesh, worldSpace = True, matrix = trans)
	cmds.setAttr(boxMesh + ".overrideEnabled", 1)
	cmds.setAttr(boxMesh + ".overrideShading", 0)
	cmds.setAttr(boxMesh + ".overrideColor", 13)
	return boxMesh


# input the joint list, create mesh boxes at each joint
def createBoxMeshList(jntList):
	boxMeshList = []
	for jnt in jntList:
		boxMeshList += [createBoxMeshAtJoint(jnt)]
	return boxMeshList


# input the boxmesh list, create box type for each box
def createBoxList(meshList):
	boxList = []
	for mesh in meshList:
		boxList += [getBoxFromMesh(mesh)]
	return boxList


# The function to skin the mesh to joints
def performSkinning(fakeInput, argList):
	
	[meshList, boxList, vertList, 
	globalArmJntList, globalMeshList, globalSkinClusterDict, 
	globalRootJnt] = argList
	infVertList = []

	# get verts into the list
	getVertsFromMesh(globalMeshList, vertList)


	# add each joint to influence 
	for index in xrange(len(boxList)):
		box = boxList[index]
		box.updateMath()

		jnt = globalArmJntList[index]

		# for each skincluster, add them one by one
		if jnt != globalRootJnt:
			for mesh in globalSkinClusterDict:
				cmds.skinCluster(globalSkinClusterDict[mesh], edit = True, 
											  		   		  addInfluence = jnt, 
											  		   		  weight = 0)

	# calculate weight for each vertex
	for vert in vertList:
		mesh = polyToTrans(vert)
		infJntList = []
		vertPosition = cmds.xform(vert, query = True, translation = True, 
										worldSpace = True)
		for index in xrange(len(boxList)):
			box = boxList[index]
			if box.insideBox(vertPosition):
				infJntList += [globalArmJntList[index]]

		# if the vert is assigned to some joint
		if infJntList != []:
			weight = 1.0/len(infJntList)

			# zip joint with skin weight
			jntWeightList = []
			for jnt in infJntList:
				jntWeightList += [(jnt, weight)]

			# set skin weight for the vertex
			cmds.skinPercent(globalSkinClusterDict[mesh], vert, 
												transformValue = jntWeightList)

# input: joint name and intended control color
# side effect: create a circle
# output: created circle's name
def createCircleAtJnt(jnt, color, prefix):
	cmds.select([])
	position = cmds.xform(jnt, query = True, worldSpace = True, matrix = True)
	control = cmds.circle(name = prefix + "temp_shape_" + jnt, normal = [-1, 0, 0])[0]
	cmds.select([])
	cmds.xform(control, matrix = position, worldSpace = True)
	return control

# input: joint name and intended control color
# side effect: create a pole vector at joint position
# output: created circle's name
def createPoleVec(jnt, color, prefix):
	cmds.select([])
	position = cmds.xform(jnt, query = True, worldSpace = True, matrix = True)
	loc = cmds.spaceLocator(name = prefix + "temp_shape_" + jnt)[0]
	cmds.xform(loc, worldSpace = True, matrix = position)
	cmds.select([])
	return loc


# input: the list of joint
# side effects: create a list of fk shapes at each joint position
# output: a list of temperory fk ctrls
def createFKArm(globalArmJntList):
	result = []
	for jnt in globalArmJntList:
		cmds.select([])

		# create circle in maya
		tempCtrl = createCircleAtJnt(jnt, "red", "FK_")
		result += [tempCtrl]

	return result



# input: fk  temp shape list, UI parent 
# side effect: add rows for fk temp controls
# output: None
def FKLayout(fkList, colLayout):
	cmds.rowLayout(numberOfColumns = 1, parent = colLayout, height = 35)
	cmds.text("FK temperory controls:")
	cmds.setParent("..")
	for tempCtrl in fkList:
		chooseButtonWrapper(colLayout, tempCtrl, tempCtrl)


# input: ik temp shape list, UI parent
# side effect: add rows for ik temp controls
# output: none
def IKLayout(ikList, colLayout):
	tempElbowCtrl = ikList[0]
	tempHandCtrl = ikList[1]

	cmds.rowLayout(numberOfColumns = 1, parent = colLayout, height = 35)
	cmds.text("IK temperory controls:")
	cmds.setParent("..")

	# pole vec layout
	chooseButtonWrapper(colLayout, tempElbowCtrl, tempElbowCtrl)

	# hand control layout
	chooseButtonWrapper(colLayout, tempHandCtrl, tempHandCtrl)

# input: ik temp shape list, UI parent
# side effect: add rows for ik temp controls
# output: none
def switchLayout(switchList, colLayout):
	switchCtrl = switchList[0]

	cmds.rowLayout(numberOfColumns = 1, parent = colLayout, height = 35)
	cmds.text("Switch temperory controls:")
	cmds.setParent("..")

	# pole vec layout
	chooseButtonWrapper(colLayout, switchCtrl, switchCtrl)


# The function to create a curve cube
def createCube(cubeName):
	cmds.select([])
	cube = cmds.curve(degree = 1, 
		p = [
		(-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), 
		(-0.5, 0.5, 0.5,), (-0.5, -0.5, 0.5,), (-0.5, -0.5, -0.5), 
		(0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5), 
		(0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), 
		(0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5)
		], 
		knot = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
		name = cubeName)
	cmds.select([])
	return cube

# input: arm joint and hand joint
# side effect: create control shape at each joint
# output: two control shapes' names
def createIKArm(armJnt, handJnt):
	poleCtrl = createPoleVec(armJnt, "red", "IK_")
	handCtrl = createCircleAtJnt(handJnt, "red", "IK_")
	return [poleCtrl, handCtrl]

def createSwitchShape(direction, handJnt):
	cubeName = createCube("temp_ctrl_" + direction + "_switch")
	position = cmds.xform(handJnt, worldSpace = True, query = True, matrix = True)
	cmds.xform(cubeName, worldSpace = True, matrix = position)
	return [cubeName]
	


# input: arm joint list
# side effect: create both fk temp controls and ik temp controls
# output: a tuple of lists of fk temp ctrl names and ik ctrl names
def createFKIKArm(direction, globalArmJntList):
	IKCtrlList = createIKArm(globalArmJntList[-2], globalArmJntList[-1])
	FKCtrlList = createFKArm(globalArmJntList)
	switchCtrlList = createSwitchShape(direction, globalArmJntList[-1])
	return (FKCtrlList, IKCtrlList, switchCtrlList)

def createSameShapeAtPosition(shapeType, tempShape, position, name):
	shape = ""
	if shapeType == "circle":
		cmds.select([])
		shape = cmds.circle(name = name, normal = [-1, 0, 0])
		cmds.select([])
	elif shapeType == "cube":
		shape = createCube(name)
	cmds.xform(shape, worldSpace = True, matrix = position)
	cmds.select(shape)
	vertNum = cmds.polyEvaluate(vertexComponent = True)
	cmds.select([])
	for i in xrange(vertNum):
		vertPosition = cmds.xform(tempShape + ".vtx[" + str(i) + "]", 
									query = True, matrix = True, 
									worldSpace = True)
		cmds.xform(shape + ".vtx[" + str(i) + "]", worldSpace = True, 
					matrix = vertPosition)
	return shape

def get_main_name(name, prefix):
	main_name = name[len(prefix):]
	print "main name is" + main_name
	return main_name

def add_prefix(name, prefix):
	new_name = prefix + name
	print "new name is " + new_name
	return new_name

# The function to add reference group out of the transform node
def zeroOut(list_objects):
	old_prefix = ""
	inserted_prefix = ""
	outer_prefix = "ref_"
	list_objects = list_objects
	num_objects = len(list_objects)

	#the returned list
	list_new_nodes = []

	#go through all the selected nodes
	for i in xrange(num_objects):
		ith_old_name = list_objects[i]
		ith_main_name = get_main_name(ith_old_name, old_prefix)
		ith_inserted_name = add_prefix(ith_main_name, inserted_prefix)
		cmds.rename(ith_old_name, ith_inserted_name)

		new_node_name = add_prefix(ith_main_name, outer_prefix)
		cmds.createNode( 'transform', name = new_node_name)

		#get the transform position
		crt_wsm = cmds.xform(ith_inserted_name, query = True, worldSpace = True, matrix = True)
		#put the transform in that position
		cmds.xform(new_node_name, worldSpace = True, matrix = crt_wsm)
		parent_name_list = cmds.listRelatives(ith_inserted_name, parent = True)
		cmds.parent(ith_inserted_name, new_node_name)
		if parent_name_list != None:
			parent_name = parent_name_list[0]
			cmds.parent(new_node_name, parent_name)
		list_new_nodes += [new_node_name]
	return list_new_nodes

#helper to zero out the control, return a list that contains all the new reference nodes
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
		ith_ik_joint = cmds.duplicate(ith_bind_name, parentOnly = True, name = ith_ik_name)
		ith_fk_joint = cmds.duplicate(ith_bind_name, parentOnly = True, name = ith_fk_name)
		ik_joint_chain += [ith_ik_joint]
		fk_joint_chain += [ith_fk_joint]
		ith_parentConstraint = cmds.parentConstraint(ith_ik_joint, ith_fk_joint, ith_bind_name)

		#connect reverse node to the fk weight
		cmds.connectAttr(reverse_node+".outputX", 
						 get_weightAttr_name(ith_parentConstraint[0], ith_fk_joint[0], "W1"))
		cmds.connectAttr(control_name + "." + attr_name, 
						 get_weightAttr_name(ith_parentConstraint[0], ith_ik_joint[0], "W0"))

	for i in xrange(num_objects-1, 0, -1):
		cmds.parent(ik_joint_chain[i], ik_joint_chain[i-1])
		cmds.parent(fk_joint_chain[i], fk_joint_chain[i-1])

	#create IK handle
	print str(ik_joint_chain[-1])
	handle = cmds.ikHandle(startJoint = ik_joint_chain[0][0], endEffector = ik_joint_chain[-1][0], solver = "ikRPsolver")[0]
	cmds.connectAttr(control_name + "." + attr_name, reverse_node+".inputX")
	return [handle, ik_joint_chain, fk_joint_chain]

# input: bunch of global lists
def rigArm(fakeInput, argList):

	# declare inputs
	[direction, 
	globalFKArmCtrlList, globalIKArmCtrlList, globalSwitchCtrlList, 
	globalArmJntList, globalFKArmJntList, globalIKArmJntList,
	globalArmControlTypeList] = argList
	# controller part:
	if globalArmControlTypeList[0] != "IK Arm":

		# the names to bew renamed
		nameList = ["ctrl_fk_" + direction + "_shoulder", 
					"ctrl_fk_" + direction + " _elbow", 
					"ctrl_fk_" + direction + "_wrist"]

		# rename all the controls
		for index in xrange(len(globalFKArmCtrlList)):
			ctrl = globalFKArmCtrlList[index]
			newName = nameList[index]

			# update the global list with the new name
			globalFKArmCtrlList[index] = cmds.rename(ctrl, newName)

		# add reference node to the transform node
		refFKNodeList = zeroOut(globalFKArmCtrlList)


	# case it's ik arm
	if globalArmControlTypeList[0] != "FK Arm":

		# the names to be renamed
		nameList = ["ctrl_ik_" + direction + "_elbow", 
					"ctrl_ik_" + direction + "_wrist"]

		# rename the controls
		for index in xrange(len(globalIKArmCtrlList)):
			ctrl = globalIKArmCtrlList[index]
			newName = nameList[index]
			globalIKArmCtrlList[index] = cmds.rename(ctrl, newName)
		# add reference node to the transform node
		refIKNodeList = zeroOut(globalIKArmCtrlList)


	# in the case for switchable arm, added another feature for switchable arm
	if (globalArmControlTypeList[0] != "IK Arm" and 
		globalArmControlTypeList[0] != "FK Arm"):

		newName = "ctrl_" + direction + "_arm_switch"
		ctrl = globalSwitchCtrlList[0]
		globalSwitchCtrlList[0] = cmds.rename(ctrl, newName)
		refSwitchNodeList = zeroOut(globalSwitchCtrlList)



	# Jnt part
	# case it's fk arm
	if globalArmControlTypeList[0] == "FK Arm":
		# parent the hieachy
		for index in xrange(len(globalFKArmCtrlList)-1):
			parentIndex = (len(globalFKArmCtrlList) - index -2)
			childIndex = (len(globalFKArmCtrlList) - index-1)
			cmds.parent(refFKNodeList[childIndex], 
						globalFKArmCtrlList[parentIndex])

		# parent joint under the controller
		for index in xrange(len(globalFKArmCtrlList)):
			cmds.parentConstraint(globalFKArmCtrlList[index], 
								globalArmJntList[index], maintainOffset = True)


	# case it's ik arm
	elif globalArmControlTypeList[0] == "IK Arm":

		# joint part:
		handle = cmds.ikHandle(startJoint = globalArmJntList[0], 
				endEffector = globalArmJntList[-1], solver = "ikRPsolver")[0]
		cmds.poleVectorConstraint(globalIKArmCtrlList[0], handle)
		cmds.pointConstraint(globalIKArmCtrlList[1], handle)


	# in the case for switchable arm, added another feature for switchable arm
	else:
		attrName = "ik_arm"
		cmds.addAttr(globalSwitchCtrlList[0], longName = attrName, 
									keyable = True, minValue = 0, maxValue = 1)
		[handle, 
		ik_joint_chain, fk_joint_chain] = createSwitch(globalSwitchCtrlList[0], 
													attrName, globalArmJntList)
		cmds.poleVectorConstraint(globalIKArmCtrlList[0], handle)
		cmds.pointConstraint(globalIKArmCtrlList[1], handle)

		for index in xrange(len(globalFKArmCtrlList)-1):
			parentIndex = (len(globalFKArmCtrlList) - index -2)
			childIndex = (len(globalFKArmCtrlList) - index-1)
			cmds.parent(refFKNodeList[childIndex], 
						globalFKArmCtrlList[parentIndex])

		# parent joint under the controller
		for index in xrange(len(globalFKArmCtrlList)):
			cmds.parentConstraint(globalFKArmCtrlList[index], 
								fk_joint_chain[index], maintainOffset = True)
		globalIKArmJntList += [ik_joint_chain]
		globalFKArmJntList += [fk_joint_chain]
		

# input: global lists
# side effects: fill in those lists and create a new window for adding controls
def addTempControllers(fakeInput, direction,
		globalFKArmCtrlList, globalIKArmCtrlList, globalSwitchCtrlList,
		globalArmJntList, globalFKArmJntList, globalIKArmJntList,
		globalArmControlTypeList):
	winName = ""
	if globalArmControlTypeList[0] == "FK Arm":
		globalFKArmCtrlList += createFKArm(globalArmJntList)
		winName = "FK setup"
	elif globalArmControlTypeList[0] == "IK Arm":
		globalIKArmCtrlList += createIKArm(globalArmJntList[-2], globalArmJntList[-1])
		winName = "IK setup"
	else:
		[fkList, ikList, switchList] = createFKIKArm(direction, globalArmJntList)
		globalFKArmCtrlList += fkList
		globalIKArmCtrlList += ikList
		globalSwitchCtrlList += switchList
		winName = "FK IK set up"
	

	# UI part
	window = cmds.window(winName, sizeable = True,
							titleBar = True, 
							resizeToFitChildren = True,
							menuBar = True,
							title = winName)
	secondColLayout = cmds.columnLayout(parent = window)

	# rows:
	# fk window option
	if globalArmControlTypeList[0] == "FK Arm":
		FKLayout(globalFKArmCtrlList, secondColLayout)
		

	# ik window option 
	elif globalArmControlTypeList[0] == "IK Arm":
		IKLayout(globalIKArmCtrlList, secondColLayout)

	# fk ik window option
	else:
		FKLayout(globalFKArmCtrlList, secondColLayout)
		IKLayout(globalIKArmCtrlList, secondColLayout)
		switchLayout(globalSwitchCtrlList, secondColLayout)

	singleButtonWrapper("", rigArm, 
		[direction, 
		globalFKArmCtrlList, globalIKArmCtrlList, globalSwitchCtrlList, 
		globalArmJntList, globalFKArmJntList, globalIKArmJntList,
		globalArmControlTypeList], "Rig the Arm")
	cmds.showWindow(window)
		

# helper to get items inside menu
def getItemInOptionMenu(item, globalArmControlTypeList):
	globalArmControlTypeList[0] = item
	print globalArmControlTypeList



# helper for delete button
# input: [[], [],  []]
def deleteNodes(fakeInput, argList):
	[deleteList] = argList
	for L in deleteList:
		cmds.delete(L)


# input locator name list, create joint chain and one box at each joint
# in addition, add buttons on UI for boxes
def createJointChainAndBox(fakeInput, argList):
	# declare inputs from the list
	[direction, locList, locParentList ,colLayout,
		globalRootJnt, globalMeshList, 
		globalArmJntList, globalFKArmJntList, globalIKArmJntList,
		globalSkinClusterDict, globalArmControlTypeList, 
		globalArmCtrlList] = argList
	# create temp lists
	vertList = []
	locatorNodeList = locList
	cmds.select([])
	locatorPosList = []
	
	globalFKArmCtrlList = globalArmCtrlList[0]
	globalIKArmCtrlList = globalArmCtrlList[1]
	globalSwitchCtrlList = globalArmCtrlList[2]
	localDeleteList = []
	for loc in locatorNodeList:
		locatorPosList += [cmds.xform(loc, query = True, translation = True, 
										   worldSpace = True)]

	# call function to create joint chain
	globalArmJntList += createJointChain(direction, 
										 locatorPosList[0], locatorPosList[1], 
										 locatorPosList[2], localDeleteList)
	# does not need to specify direction
	meshList = createBoxMeshList(globalArmJntList)
	# does not need to specify direction
	boxList = createBoxList(meshList)
	# UI part
	for meshName in meshList:
		chooseButtonWrapper(colLayout, meshName, meshName)

	singleButtonWrapper("", performSkinning, 
		[meshList, boxList, vertList, 
		globalArmJntList, globalMeshList, globalSkinClusterDict, globalRootJnt], 
		"Add Influence")

# Special layout with 2 cols
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 15), (2, "both", 15)], 
					columnWidth = [(1, 300), (2, 250)],
					height = 35 )
	cmds.optionMenu( label = "Control Type", changeCommand = 
		partial(getItemInOptionMenu,
			globalArmControlTypeList = globalArmControlTypeList
		)
	)
	cmds.menuItem(label = "FK Arm")
	cmds.menuItem(label = "IK Arm")
	cmds.menuItem(label = "FK IK Switchable Arm")

	cmds.button( label = "Create Control Shapes", command = 
		partial(
			addTempControllers,
				direction = direction,
				globalArmControlTypeList = globalArmControlTypeList,
				globalArmJntList = globalArmJntList,
				globalFKArmJntList = globalFKArmJntList,
				globalIKArmJntList = globalIKArmJntList,
				globalFKArmCtrlList = globalFKArmCtrlList,
				globalIKArmCtrlList = globalIKArmCtrlList,
				globalSwitchCtrlList = globalSwitchCtrlList
		)
	)
	cmds.setParent("..")
# end of special layout

	singleButtonWrapper("", deleteNodes, [[meshList, locList, locParentList, 
										  localDeleteList]],
		"Delete Helper Nodes")


	cmds.setParent("..")


# function for creating locators
def createLocators(fakeInput, argList):
	[num, direction, locList, locParentList, colLayout,
	globalRootJnt, globalMeshList, 
	globalArmJntList, globalFKArmJntList, globalIKArmJntList,
	globalSkinClusterDict, globalArmControlTypeList, 
	globalArmCtrlList] = argList
	print direction
	locatorPrefix = "armLocator_temp_" + direction + "_"
	locatorParentPrefix = "armLocator_tempParent_" + direction
	# for the number of creators
	for i in xrange(num):
		# create locator
		locName = cmds.spaceLocator(name = locatorPrefix + str(i+1))[0]
		locList += [locName]
		cmds.select([])
		# do UI part
		chooseButtonWrapper("", locName, locName)
	locParentList += [createCube(locatorParentPrefix)]
	chooseButtonWrapper("", locatorParentPrefix, locatorParentPrefix)
	cmds.xform(locParentList[0], translation = [3.305, 0.269, -0.426], 
								 scale = [8.204, 2.916, 3.791])
	cmds.xform(locList[0], translation = [0, 0, 0])
	cmds.xform(locList[1], translation = [3.479, 0, -1.877])
	cmds.xform(locList[2], translation = [6.843, 0, 0])
	for i in xrange(num):
		cmds.parent(locList[i], locParentList[0])
	if direction == "r":
		tempParentLocator = cmds.spaceLocator()
		cmds.parent(locParentList[0], tempParentLocator)
		cmds.xform(tempParentLocator, scale = [-1, 1, 1])
		cmds.parent(locParentList[0], world = True)
		# cmds.deleteNodes(tempParentLocator)


	singleButtonWrapper("", createJointChainAndBox, 
		[direction, locList, locParentList, colLayout,
		globalRootJnt, globalMeshList, 
		globalArmJntList, globalFKArmJntList, globalIKArmJntList, 
		globalSkinClusterDict, globalArmControlTypeList, globalArmCtrlList], 
		"Confirm Locators")

# The real UI function
# Notice that the arm control list is in the format [fkList, ikList, switchList]
def armWin(fakeInput,
			globalRootJntList, globalMeshList, 
			globalArmJntList, globalFKArmJntList, globalIKArmJntList,
			globalSkinClusterDict, globalArmControlTypeList, globalArmCtrlList, 
			globalDirectionList):
	win_Name = "PandaMenu Auto Rigging Tool - Arm"
	versionNumber = 0.1

	#if old ui not closed, close it
	if cmds.window(win_Name, exists = True):
		cmds.deleteUI(win_Name)
	window = cmds.window(win_Name, sizeable = True,
							titleBar = True, resizeToFitChildren = True,
							menuBar = True,
							title = win_Name + " ver " + str(versionNumber))

	locList = []
	locParentList = []
	globalRootJnt = globalRootJntList[0]
	direction = globalDirectionList[0]
	#col layout
	colLayout = cmds.columnLayout()

	singleButtonWrapper("", createLocators, 
		[3, direction, locList, locParentList, colLayout, 
		globalRootJnt, globalMeshList, 
		globalArmJntList, globalFKArmJntList, globalIKArmJntList,
		globalSkinClusterDict, globalArmControlTypeList, globalArmCtrlList],
		"CreateLocators")

	cmds.showWindow( window )
# For test's sake
# sk = dict([])
# sk["polySurface2"] = "skinCluster1"
# armWin("", "joint1", ["polySurface2"], [], sk, ["FK Arm"], [], ["r"])