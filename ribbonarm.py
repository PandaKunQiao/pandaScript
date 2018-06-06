#cumstom menu by Fred Qiao
import maya.cmds as cmds
from functools import partial
import maya.mel as mel
import math



##################################################################################
#								  Nurb Helpers							     	 #
##################################################################################



def createCircle(trans, rot, input_circle_name):
	circle_name = cmds.circle(center = [0, 0, 0], name = input_circle_name)
	ref_name = cmds.createNode("transform", name = "ref_" + input_circie_name)
	cmds.xform(ref_name, matrix = matr, worldSpace = True)
	return circle_name


def createDiamond(matr, input_diamond_name):
	diamond_name = cmds.curve(name = input_diamond_name, degree = 1, 
							  point = [(0, 0, 1), (0, 1, 0), (0, 0, -1), (0, -1, 0), (0, 0, 1)])
	ref_name = cmds.createNode("transform", name = "ref_" + input_diamond_name)
	cmds.parent(diamond_name, ref_name)
	cmds.xform(ref_name, matrix = matr, worldSpace = True)
	return diamond_name

def createDistance(start, end, distName):
	distNode = cmds.createNode("distanceDimShape")
	transNode = cmds.listRelatives(distNode, parent = True)
	cmds.select(transNode)
	cmds.rename(distName)
	distNode = cmds.ls(selection = True)[0]
	up_loc = cmds.spaceLocator(name = "loc_" + distName + "_up")[0]
	bot_loc = cmds.spaceLocator(name = "loc_" + distName + "_bot")[0]
	cmds.parentConstraint(start, up_loc, maintainOffset = False)
	cmds.parentConstraint(end, bot_loc, maintainOffset = False)
	cmds.connectAttr(up_loc+".translate", distNode+"Shape"+".startPoint")
	cmds.connectAttr(bot_loc+".translate", distNode+"Shape"+".endPoint")
	dist_num = cmds.getAttr(distNode+"Shape"+".distance")
	return (dist_num, distNode+"Shape")

def createMult(input1, type1, input2, type2, calc, suffix):
	mult_node = cmds.createNode("multiplyDivide", name = calc + suffix)
	if type1 == "connect":
		cmds.connectAttr(input1[0], mult_node+".input1X")
		cmds.connectAttr(input1[1], mult_node+".input1Y")
		cmds.connectAttr(input1[2], mult_node+".input1Z")
	elif type1 == "value":
		cmds.setAttr(mult_node+".input1X", input1[0])
		cmds.setAttr(mult_node+".input1Y", input1[1])
		cmds.setAttr(mult_node+".input1Z", input1[2])
	if type2 == "connect":
		cmds.connectAttr(input2[0], mult_node+".input2X")
		cmds.connectAttr(input2[1], mult_node+".input2Y")
		cmds.connectAttr(input2[2], mult_node+".input2Z")
	elif type2 == "value":
		cmds.setAttr(mult_node+".input2X", input2[0])
		cmds.setAttr(mult_node+".input2Y", input2[1])
		cmds.setAttr(mult_node+".input2Z", input2[2])
	if calc == "mult":
		cmds.setAttr(mult_node+".operation", 1)
	elif calc == "div":
		cmds.setAttr(mult_node+".operation", 2)
	else:
		cmds.setAttr(mult_node+".operation", 3)
	return mult_node


##################################################################################
#							Main Procedure Helpers							     #
##################################################################################



#helper to get text in field
def get_text(tfd_name1, tfd_name2, tfd_name3, tfd_name4, tfd_name5):
	global_prefix_name_list = [cmds.textField(tfd_name1, query = True, text = True),
							   cmds.textField(tfd_name2, query = True, text = True),
							   cmds.textField(tfd_name3, query = True, text = True),
							   cmds.textField(tfd_name4, query = True, text = True),
							   cmds.textField(tfd_name5, query = True, text = True)]
	print "inputs are " + str(global_prefix_name_list)
	return global_prefix_name_list

def get_main_name(name, prefix):
	main_name = name[len(prefix):]
	print "main name is" + main_name
	return main_name

def add_prefix(name, prefix):
	new_name = prefix + name
	print "new name is " + new_name
	return new_name




##################################################################################
#						 Selected Transformation Nodes Window 					 #
##################################################################################






def calcAngle(pos1, pos2, direction):
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
	return cmds.getAttr(temp_angle + ".euler")[0]
	# if direction == "z":
	# 	x = pos1[0] - pos2[0]
	# 	y = pos1[1] - pos2[1]
	# elif direction == "x":
	# 	x = pos1[2] - pos2[2]
	# 	y = pos1[1] - pos2[1]
	# z_angle = abs(math.degrees(math.atan2(abs(y), abs(x))))
	# if (x > 0 and y > 0):
	# 	z_angle = z_angle
	# if (x > 0 and y < 0):
	# 	z_angle = -z_angle
	# if (x < 0 and y > 0):
	# 	z_angle = -z_angle
	# else:
	# 	z_angle = z_angle
	# if direction == "z":
	# 	return [0, 0, z_angle]
	# elif direction == "x":
	# 	return [0, 90, z_angle]


#helper to show which transform node is selected
def fill_selected_object(loc_container, trans_container, *args):
	name_window = cmds.window("Selected Locators", 
							   sizeable = True,
							   widthHeight = (300, 800),
							   title = "Selected Joints")
	print "name of the window: "
	print name_window
	list_objects = cmds.ls(selection = True)
	loc_container += list_objects
	cmds.columnLayout(columnAttach=("left", 5))
	for i in xrange(len(list_objects)):
		cmds.rowLayout(numberOfColumns = 1, 
					   columnAttach = [(1, "both", 0)],
					   columnWidth = [(1, 300)],
					   height = 40)
		cmds.text(label = list_objects[i])
		cmds.setParent("..")
	cmds.rowLayout(numberOfColumns = 1, 
				   columnAttach = [(1, "both", 0)],
				   columnWidth = [(1, 300)],
				   height = 40)
	pos1 = cmds.xform(list_objects[0], query = True, translation = True)
	pos2 = cmds.xform(list_objects[1], query = True, translation = True)
	angle = calcAngle(pos1, pos2, "x")
	trans = [(pos1[0] + pos2[0])/2.0, (pos1[1] + pos2[1])/2.0, (pos1[2] + pos2[2])/2.0]
	scale = [((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2 + (pos1[2] - pos2[2])**2)**0.5, 1, 1]
	trans_container += [trans, angle, scale]
	# createNurb(angle, trans, scale, "a")
	

	cmds.text(str(angle))
	cmds.setParent("..")
	cmds.showWindow(name_window)
	cmds.setParent("..")






##################################################################################
#					       New Transform Reference Nodes   						 #
##################################################################################



def createNurb(trans, angle, scale, transName, *args):
	nurb = cmds.nurbsPlane(patchesU = 9, patchesV = 1, degree = 1, name = transName, axis = [0, 1, 0], width = 1)
	cmds.xform(nurb, rotation = angle, translation = trans, scale = scale)
	return nurb

def computeDistance(trans1, trans2):
	pos1 = cmds.xform(trans1, query = True, translation = True)
	pos2 = cmds.xform(trans2, query = True, translation = True)
	return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 + (pos1[2] - pos2[2])**2)



#function that triggered when hit the confirm button
def second_button(tfd_name_list, trans_list, loc_list, *args):
	# if cmds.window("Selected_Joints", exists = True):
	# 	cmds.deleteUI("Selected_Joints")
	plane_name = cmds.textField(tfd_name_list[0], query = True, text = True)
	suffix_name = cmds.textField(tfd_name_list[3], query = True, text = True)
	joint_name = cmds.textField(tfd_name_list[2], query = True, text = True)
	drv_joint_name = cmds.textField(tfd_name_list[1], query = True, text = True)
	orientation = cmds.textField(tfd_name_list[4], query = True, text = True)

	nurb = createNurb(trans_list[0], trans_list[1], trans_list[2], plane_name)
	mel.eval("createHair 9 1 2 0 0 0 0 5 0 1 1 1")
	shapeNode = cmds.listRelatives(nurb, shapes = True)[0]
	follicle_list = cmds.listConnections(shapeNode, type = "follicle", shapes = True)
	print follicle_list
	sys_node = cmds.listConnections(follicle_list[0], type = "hairSystem", shapes = True)
	print sys_node
	sys_trans = cmds.listRelatives(sys_node, parent = True)
	print sys_trans
	nuc_node = cmds.listConnections(sys_node, type = "nucleus", shapes = True)
	print nuc_node
	pfx_node = cmds.listConnections(sys_node, type = "pfxHair", shapes = True)
	print pfx_node
	pfx_trans = cmds.listRelatives(pfx_node, parent = True)
	print pfx_trans
	cmds.delete(pfx_trans + sys_trans + nuc_node)
	follicle_trans_list = cmds.listConnections(shapeNode, type = "follicle")[0:9]
	print shapeNode
	print follicle_trans_list
	follicle_group = cmds.listRelatives(follicle_trans_list[0], parent = True)
	follicle_tuple_list = []

	for i in xrange(len(follicle_trans_list)):
		crt_follicle = follicle_trans_list[i]
		follicle_tuple_list += [(crt_follicle, computeDistance(crt_follicle, loc_list[0]))]
	follicle_tuple_list = sorted(follicle_tuple_list, key=lambda follicle: follicle[1])
	print follicle_tuple_list
	bn_joint_list = []

	for i in xrange(len(follicle_trans_list)):
		print i
		print follicle_trans_list[i]
		crt_follicle = follicle_tuple_list[i][0]
		crt_pos = cmds.xform(crt_follicle, query = True, matrix = True, worldSpace = True)
		cmds.select(clear = True)
		crt_joint = cmds.joint(name = joint_name + str(i+1))
		cmds.xform(crt_joint, matrix = crt_pos, worldSpace = True)
		cmds.makeIdentity(rotate = True)
		crt_constraint = cmds.parentConstraint(crt_follicle, crt_joint, maintainOffset = True)
		cmds.setAttr(crt_constraint[0]+".interpType", 2)
		bn_joint_list += [crt_joint]

	follicle_group = cmds.rename(follicle_group, "grp_follicle_" + suffix_name)

	# joints and controls in order that from to to the bottom
	drv_joint_list = []
	bend_ctrl_list = []

	for i in xrange(5):
		crt_bn = bn_joint_list[2*i]
		crt_pos = cmds.xform(crt_bn, translation = True, query = True)
		cmds.select(clear = True)
		crt_drv_joint = cmds.joint(name = drv_joint_name +str(i+1))
		cmds.xform(crt_drv_joint, translation = crt_pos)
		drv_joint_list += [crt_drv_joint]

	for i in range(4, 0, -1):
		cmds.parent(drv_joint_list[i], drv_joint_list[i-1])
		cmds.joint(drv_joint_list[i-1], edit = True, orientJoint = "xzy", secondaryAxisOrient = "xup", zeroScaleOrient = True)
		matr = cmds.xform(drv_joint_list[i-1], query = True, matrix = True, worldSpace = True)
		# ctrl_bend_suffix_#
		crt_diamond_name = createDiamond(matr, "ctrl_bend" + suffix_name + "_" + str(i))
		bend_ctrl_list = [crt_diamond_name] + bend_ctrl_list
		cmds.parentConstraint(crt_diamond_name, drv_joint_list[i-1], maintainOffset = True)

	# create the last joint and controller 
	cmds.select(drv_joint_list[-1])
	cmds.joint(orientation = [0, 0, 0], edit = True)
	

	last_diamond_name = createDiamond(matr, "ctrl_bend"+suffix_name+"_"+str(5))
	
	bend_ctrl_list = bend_ctrl_list + [last_diamond_name]

	for i in range(0, 4):
		cmds.parent(drv_joint_list[i]+"|"+drv_joint_list[i+1], world = True)
	last_trans = cmds.xform(drv_joint_list[4], query = True, translation = True, worldSpace = True)
	cmds.xform(last_diamond_name, translation = last_trans, worldSpace = True)
	cmds.parentConstraint(last_diamond_name, drv_joint_list[4], maintainOffset = True)

	#create the volume conservation system for ribbon
	dist_num_node = createDistance(bend_ctrl_list[0], bend_ctrl_list[-1], "dist" + suffix_name)
	div_node = createMult([dist_num_node[0], 1, 1], "value", 
						  [dist_num_node[1]+".distance", dist_num_node[1]+".distance", dist_num_node[1]+".distance"], "connect", 
						  "div", suffix_name)
	print div_node
	pow_node = createMult([div_node + ".outputX", div_node + ".outputY", div_node + ".outputZ"], "connect", [0.5, 0.5, 0.5], "value", "power", suffix_name)
	for bn_joint in bn_joint_list:
		cmds.connectAttr(pow_node+".outputX", bn_joint+".scale.scaleY")
		cmds.connectAttr(pow_node+".outputX", bn_joint+".scale.scaleZ")

	sc = cmds.skinCluster(drv_joint_list + [nurb[0]], dropoffRate =7, toSelectedBones = True)





##################################################################################
#     							Main Procedure   								 #
##################################################################################




def win(fakeinput = True):
	win_Name = "PandaMenu Create Ribbon Arm"
	versionNumber = 0.1

	#if old ui not closed, close it
	if cmds.window(win_Name, exists = True):
		cmds.deleteUI(win_Name)
	window = cmds.window(win_Name, sizeable = True,
							titleBar = True, resizeToFitChildren = False,
							menuBar = True,
							title = win_Name + " ver " + str(versionNumber))

	#global list that contains cross-window selection names
	control_name_space_list = []
	joint_list = []
	loc_list = []
	trans_list = []
	#col layout
	cmds.columnLayout(columnAttach=('left', 5))

	#first row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Select transform node ' )
	cmds.button(label = "Confirm", command = partial(fill_selected_object, loc_list, trans_list))
	cmds.setParent("..")


	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Plane Name' )
	fst_textfield = cmds.textField(text = "plane_")
	cmds.setParent("..")

	#second row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Driver joint prefix' )
	scd_textfield = cmds.textField(text = "drv_")
	cmds.setParent("..")

	#third row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Binding Joint Prefix' )
	thd_textfield = cmds.textField(text = "bn_")
	cmds.setParent("..")

	#reverse node row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Non DAG node name suffix' )
	frth_textfield = cmds.textField(text = "_ribbon")
	cmds.setParent("..")


	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	control_name_space = cmds.text( label = "Joint Orientation" )
	ffth_textfield = cmds.textField(text = "xzx")
	cmds.setParent("..")

	#the button
	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=[(1, 'both', 0)],
					columnWidth = (1, 400), 
					height = 50 )
	cmds.button(label = "Create Ribbon Arm", command = partial(second_button, 
															   [fst_textfield, scd_textfield, 
															    thd_textfield, frth_textfield,
															    ffth_textfield],
															   	trans_list,
															   	loc_list))
	cmds.showWindow( window )
