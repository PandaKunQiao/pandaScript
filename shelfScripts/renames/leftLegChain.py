import maya.cmds as cmds

LEGJNTCHAIN = ["sk_l_femur_jnt", "sk_l_knee_jnt", "sk_l_ankle_jnt"]
def renameNodeChain(nmLs):
	renameNodeLs = cmds.ls(selection = True)
	for i in xrange(len(renameNodeLs)):
		node = renameNodeLs[i]
		newNm = nmLs[i]
		cmds.rename(node, newNm)


renameNodeChain(LEGJNTCHAIN)