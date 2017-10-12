#cumstom menu by Fred Qiao
import maya.cmds as cmds
from functools import partial


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

#helper to zero out the control, return a list that contains all the new reference nodes
def createSwitch(tfd_name_list, joint_list):
	tfd_name1 = tfd_name_list[0]
	tfd_name2 = tfd_name_list[1]
	tfd_name3 = tfd_name_list[2]
	tfd_name4 = tfd_name_list[3]
	tfd_name5 = tfd_name_list[4]
	txt_name = tfd_name_list[5]
	[bind_prefix, ik_prefix, fk_prefix, reverse_name, attr_name] = get_text(tfd_name1, tfd_name2, tfd_name3, tfd_name4, tfd_name5)
	control_name = cmds.text(txt_name, query = True, label = True)
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
		print ik_joint_chain[i-1]
		cmds.parent(ik_joint_chain[i], ik_joint_chain[i-1])
		cmds.parent(fk_joint_chain[i], fk_joint_chain[i-1])
	cmds.connectAttr(control_name + "." + attr_name, reverse_node+".inputX")
	return [reverse_node]


#function that triggered when hit the confirm button
def second_button(tfd_name_list, joint_list, *args):
	if cmds.window("Selected_Joints", exists = True):
		cmds.deleteUI("Selected_Joints")
	reverse_node_list = createSwitch(tfd_name_list, joint_list)
	select_reverse_window(reverse_node_list)




##################################################################################
#					  fill the selected control to space   						 #
##################################################################################



#helper to show the selected control item after confirming the control that contains 
#fkik switch attribute
def fill_selection_button(space_name_list, *args):
	space_name = space_name_list[0]
	control_name_list = cmds.ls(selection = True)
	control_name = control_name_list[0]
	cmds.text(space_name, edit = True, label = control_name)
	return control_name





##################################################################################
#     							Main Procedure   								 #
##################################################################################




def win(fakeinput = True):
	win_Name = "PandaMenu Create FKIK Switch"
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
	#col layout
	cmds.columnLayout(columnAttach=('left', 5))

	#first row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Select transform node ' )
	cmds.button(label = "Confirm", command = partial(fill_selected_object, joint_list))
	cmds.setParent("..")


	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Bind Joint Prefix' )
	fst_textfield = cmds.textField(text = "bn_")
	cmds.setParent("..")

	#second row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'IK Joint Prefix' )
	scd_textfield = cmds.textField(text = "ik_")
	cmds.setParent("..")

	#third row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'FK Joint Prefix' )
	thd_textfield = cmds.textField(text = "fk_")
	cmds.setParent("..")

	#reverse node row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Reverse Node Name' )
	frth_textfield = cmds.textField(text = "rev_")
	cmds.setParent("..")

	#control node row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Select the Control' )
	cmds.button(label = "Confirm Selection", command = partial(fill_selection_button, control_name_space_list))
	cmds.setParent("..")

	#attribute name row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = "Control Name" )
	cmds.text( label = "Attribute Name")
	cmds.setParent("..")

	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	control_name_space = cmds.text( label = "" )
	control_name_space_list += [control_name_space]
	ffth_textfield = cmds.textField()
	cmds.setParent("..")

	#the button
	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=[(1, 'both', 0)],
					columnWidth = (1, 400), 
					height = 50 )
	cmds.button(label = "Create Switch", command = partial(second_button, [fst_textfield, scd_textfield, thd_textfield, frth_textfield, ffth_textfield, control_name_space], joint_list))
	cmds.showWindow( window )
win()# fk-ik-switch-create-tool
