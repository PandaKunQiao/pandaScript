import maya.cmds as cmds

SPINEJNTCHAIN = ["sk_hips_jnt", "sk_spine_A_jnt", "sk_spine_B_jnt", "sk_spine_C", "sk_chest_jnt"]

def renameNodeChain(nmLs):
	renameNodeLs = cmds.ls(selection = True)
	for i in xrange(len(renameNodeLs)):
		node = renameNodeLs[i]
		newNm = nmLs[i]
		cmds.rename(node, newNm)


renameNodeChain(SPINEJNTCHAIN)