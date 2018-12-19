import maya.cmds as cmds

jntLs = cmds.ls(selection = True)
for i in xrange(len(jntLs)):
	jnt = jntLs[i]
	ctrl = cmds.duplicate("orig_ctrl", name = jnt[:-3] + "_ctrl")
	ref = cmds.createNode("transform", name = ctrl + "_ref")
	cmds.parent(ctrl, ref)
	tempConstraint = cmds.parentConstraint(jnt, ref, maintainOffset = False)
	cmds.delete(tempConstraint)
