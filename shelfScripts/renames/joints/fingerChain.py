import maya.cmds as cmds
def renameNodeChain(nmLs):
	renameNodeLs = cmds.ls(selection = True)
	for i in xrange(len(renameNodeLs)):

		node = renameNodeLs[i]
		print node
		newNm = nmLs[i]
		cmds.rename(node, newNm)

FINGERCTRLCHAIN = (["sk_l_thumb_A_jnt", "sk_l_thumb_B_jnt", "sk_l_thumb_C_jnt", 
					"sk_l_index_A_jnt", "sk_l_index_B_jnt", "sk_l_index_C_jnt", 
					"sk_l_middle_A_jnt", "sk_l_middle_B_jnt", "sk_l_middle_C_jnt", 
					"sk_l_ring_A_jnt", "sk_l_ring_B_jnt", "sk_l_ring_C_jnt", 
					"sk_l_little_A_jnt", "sk_l_little_B_jnt", "sk_l_little_C_jnt"])

renameNodeChain(FINGERCTRLCHAIN)