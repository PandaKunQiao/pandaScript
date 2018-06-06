#cumstom menu by Fred Qiao
import maya.cmds as cmds
from functools import partial


##################################################################################
#							Main Procedure Helpers							     #
##################################################################################



#helper to get text in field
def get_text(tfd_name1, tfd_name2, tfd_name3):
	global_prefix_name_list = [cmds.textField(tfd_name1, query = True, text = True),
							   cmds.textField(tfd_name2, query = True, text = True),
							   cmds.textField(tfd_name3, query = True, text = True)]
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
def fill_selected_object(*args):
	name_window = cmds.window("Selected Transformation Nodes", 
							   sizeable = True,
							   widthHeight = (300, 800),
							   title = "Selected Transformation Nodes")
	print "name of the window: "
	print name_window
	list_objects = cmds.ls(selection = True)
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
def close_newref_window(*args):
	cmds.deleteUI("New_Transform_Reference_Nodes")

#helper to create window that contains new reference nodes and selecting buttons
def select_newref_window(new_ref_list):
	name_window = cmds.window("New Transform Reference Nodes", 
							   sizeable = True,
							   widthHeight = (300, 800),
							   title = "New Transform Reference Nodes")
	cmds.columnLayout(columnAttach=("left", 5))
	for i in xrange(len(new_ref_list)):
		cmds.rowLayout(numberOfColumns = 2,
					   columnAttach = [1, "both", 0],
					   columnWidth = [(1, 300)],
					   height = 40)
		cmds.text(label = new_ref_list[i])
		cmds.button(label = "Select", command = partial(select_node, new_ref_list[i]))
		cmds.setParent("..")
	cmds.rowLayout(numberOfColumns = 1,
				   columnAttach = [1, "both", 0],
				   columnWidth = [(1, 300)],
				   height = 40)
	cmds.button(label = "Close", command = partial(close_newref_window))
	cmds.setParent("..")
	cmds.showWindow(name_window)
	cmds.setParent("..")

#helper to zero out the control, return a list that contains all the new reference nodes
def zero_out(tfd_name_list):
	tfd_name1 = tfd_name_list[0]
	tfd_name2 = tfd_name_list[1]
	tfd_name3 = tfd_name_list[2]
	[old_prefix, inserted_prefix, outer_prefix] = get_text(tfd_name1, tfd_name2, tfd_name3)
	list_objects = cmds.ls(selection = True)
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
		print parent_name_list
		if parent_name_list != None:
			parent_name = parent_name_list[0]
			cmds.parent(new_node_name, parent_name)
		list_new_nodes += [new_node_name]
	return list_new_nodes


#function that triggered when hit the confirm button
def second_button(tfd_name_list, *args):
	if cmds.window("Selected_Transformation_Nodes", exists = True):
		cmds.deleteUI("Selected_Transformation_Nodes")
	new_ref_list = zero_out(tfd_name_list)
	select_newref_window(new_ref_list)





##################################################################################
#     							Main Procedure   								 #
##################################################################################




def win(fakeinput = True):
	win_Name = "PandaMenu Zero Out"
	versionNumber = 0.1

	#if old ui not closed, close it
	if cmds.window(win_Name, exists = True):
		cmds.deleteUI(win_Name)
	window = cmds.window(win_Name, sizeable = True,
							titleBar = True, resizeToFitChildren = False,
							menuBar = True,
							title = win_Name + " ver " + str(versionNumber))

	#col layout
	cmds.columnLayout(columnAttach=('left', 5))

	#first row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Select transform node ' )
	cmds.button(label = "Confirm", command = partial(fill_selected_object))
	cmds.setParent("..")


	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Old Prefix Name' )
	fst_textfield = cmds.textField()
	cmds.setParent("..")

	#second row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Inserted Prefix Name' )
	scd_textfield = cmds.textField()
	cmds.setParent("..")

	#third row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Outer Prefix Name' )
	thd_textfield = cmds.textField()
	cmds.setParent("..")

	#the button
	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=[(1, 'both', 0)],
					columnWidth = (1, 400), 
					height = 50 )
	print cmds.textField(fst_textfield, query = True, text = True)
	cmds.button(label = "Zero Out", command = partial(second_button, [fst_textfield, scd_textfield, thd_textfield]))
	cmds.showWindow( window )