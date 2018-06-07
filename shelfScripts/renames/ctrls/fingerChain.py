import maya.cmds as cmds
def renameNodeChain(nmLs):
	renameNodeLs = cmds.ls(selection = True)
	for i in xrange(len(renameNodeLs)):
		node = renameNodeLs[i]
		newNm = nmLs[i]
		cmds.rename(node, newNm)

FINGERCTRLCHAIN = (["ctrl_l_thumb_A", "ctrl_l_thumb_B", "ctrl_l_thumb_C", 
					"ctrl_l_index_A", "ctrl_l_index_B", "ctrl_l_index_C", 
					"ctrl_l_middle_A", "ctrl_l_middle_B", "ctrl_l_middle_C", 
					"ctrl_l_ring_A", "ctrl_l_ring_B", "ctrl_l_ring_C", 
					"ctrl_l_little_A", "ctrl_l_little_B", "ctrl_l_little_C"])

renameNodeChain(FINGERCTRLCHAIN)