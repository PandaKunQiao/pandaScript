#cumstom menu by Fred Qiao
import maya.cmds as cmds
from functools import partial


##################################################################################
#							Main Procedure Helpers							     #
##################################################################################


def get_main_name(name, prefix):
	main_name = name[len(prefix):]
	print "main name is" + main_name
	return main_name

def add_prefix(name, prefix):
	new_name = prefix + name
	print "new name is " + new_name
	return new_name



#helper to zero out the control, return a list that contains all the new reference nodes
def quick_zero_out():
	old_prefix = ""
	inserted_prefix = ""
	outer_prefix = "ref_"
	list_objects = cmds.ls(selection = True)
	num_objects = len(list_objects)

	#the returned list
	list_new_nodes = []

	#go through all the selected nodes
	for i in xrange(num_objects):
		ith_old_name = list_objects[i]
		if ith_old_name[0:3] == "ref":
			old_prefix = "ref_"
			inserted_prefix = "space_"
			outer_prefix = "ref_"
		else:
			old_prefix = ""
			inserted_prefix = ""
			outer_prefix = "ref_"
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


##################################################################################
#     							Main Procedure   								 #
##################################################################################

quick_zero_out()

