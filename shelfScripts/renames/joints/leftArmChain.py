import maya.cmds as cmds

ARMJNTCHAIN = ["sk_l_shoulder_jnt", "sk_l_elbow_jnt", "sk_l_wrist_jnt"]
def renameNodeChain(nmLs):
	renameNodeLs = cmds.ls(selection = True)
	for i in xrange(len(renameNodeLs)):
		node = renameNodeLs[i]
		newNm = nmLs[i]
		cmds.rename(node, newNm)


renameNodeChain(ARMJNTCHAIN)