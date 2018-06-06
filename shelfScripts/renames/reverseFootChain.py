import maya.cmds as cmds

def renameNodeChain(nmLs):
	renameNodeLs = cmds.ls(selection = True)
	for i in xrange(len(renameNodeLs)):
		node = renameNodeLs[i]
		newNm = nmLs[i]
		cmds.rename(node, newNm)


renameNodeChain(["rf_l_outFoot_jnt", "rf_l_inFoot_jnt", "rf_l_heel_jnt", "rf_l_toe_jnt", "rf_l_ball_jnt", "rf_l_ankle_jnt"])