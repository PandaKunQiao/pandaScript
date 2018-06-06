import string
control_list = cmds.ls(selection = True)
for i in xrange(len(control_list)):
	crt_transform = control_list[i]
	new_node_name = "norm_" + crt_transform[5:]
	counter_node_name = "counter_" + control_list[i]
	norm_node = cmds.createNode( 'multiplyDivide', name = new_node_name)
	cmds.connectAttr(control_list[i]+".translate", norm_node+".input1")
	cmds.setAttr(norm_node+".input2", -1, -1, -1, type = "double3")
	cmds.connectAttr(norm_node + ".output", counter_node_name + ".translate")

	jnt_name = ("jnt_" + crt_transform[5:]).lower()
	cmds.connectAttr(control_list[i]+".translate", jnt_name+".translate")
	cmds.connectAttr(control_list[i]+".rotate", jnt_name+".rotate")
	cmds.connectAttr(control_list[i]+".scale", jnt_name+".scale")