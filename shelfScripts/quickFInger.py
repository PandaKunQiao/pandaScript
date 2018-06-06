import maya.cmds as cmds

# Requires to select the hand cotrol that finger attributeds are on

FINGERATTRLS = [("custom_attributes", "enum", ("_________", 0)),
				("fist", "float", 0),
				("neutral", "float", 0),
				("claw", "float", 0),
				("bind", "float", 0)]

FINGERREFCHAIN = ["ref_ctrl_l_thumb_A", "ref_ctrl_l_thumb_B", "ref_ctrl_l_thumb_C", 
					"ref_ctrl_l_index_A", "ref_ctrl_l_index_B", "ref_ctrl_l_index_C", 
					"ref_ctrl_l_middle_A", "ref_ctrl_l_middle_B", "ref_ctrl_l_middle_C", 
					"ref_ctrl_l_ring_A", "ref_ctrl_l_ring_B", "ref_ctrl_l_ring_C", 
					"ref_ctrl_l_little_A", "ref_ctrl_l_little_B", "ref_ctrl_l_little_C"]

FINGERCTRLCHAIN = ["ctrl_l_thumb_A", "ctrl_l_thumb_B", "ctrl_l_thumb_C", 
					"ctrl_l_index_A", "ctrl_l_index_B", "ctrl_l_index_C", 
					"ctrl_l_middle_A", "ctrl_l_middle_B", "ctrl_l_middle_C", 
					"ctrl_l_ring_A", "ctrl_l_ring_B", "ctrl_l_ring_C", 
					"ctrl_l_little_A", "ctrl_l_little_B", "ctrl_l_little_C"]
def get_main_name(name, prefix):
	main_name = name[len(prefix):]
	print "main name is" + main_name
	return main_name

def add_prefix(name, prefix):
	new_name = prefix + name
	print "new name is " + new_name
	return new_name



#helper to zero out the control, return a list that contains all the new reference nodes
def fingerZeroOut(old_prefix, inserted_prefix, outer_prefix):
	list_objects = FINGERREFCHAIN
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


def addAttrToCtrl(trsNode, attrTupleLs):
	for attrTuple in attrTupleLs:
		attrNm = attrTuple[0]
		attrType = attrTuple[1]
		attrDefVal = attrTuple[2]
		if attrType == "float":
			cmds.addAttr(trsNode, longName = attrNm, attributeType = attrType, 
				hidden=False, defaultValue=attrDefVal)
		else:
			cmds.addAttr(trsNode, longName = attrNm, hidden = False, 
				attributeType = attrType, enumName = attrDefVal[0], 
				defaultValue = attrDefVal[1])
		cmds.setAttr(trsNode + "." + attrNm, edit = True, keyable = True)
	return None

addAttrToCtrl(cmds.ls(selection = True)[0], FINGERATTRLS)
fingerZeroOut("ref_", "fist_", "ref_")
fingerZeroOut("ref_", "neutral_", "ref_")
fingerZeroOut("ref_", "claw_", "ref_")
fingerZeroOut("ref_", "bind_", "ref_")
fingerZeroOut("ref_", "curl_", "ref_")
fingerZeroOut("ref_", "shear_", "ref_")