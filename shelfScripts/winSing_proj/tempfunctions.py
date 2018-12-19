import maya.cmds as cmds
def addAimConstraints(rotJntLs):
	for i in xrange(len(refJntLs)):
		refJnt = refJntLs[i]
		aimJnt = refJnt[:-7] + "_aim"
		upperRotJnt = refJnt[:-7] + "_upperParent_rot"
		lowerRotJnt = refJntLs[:-7] + "_lowerParent_rot"
		aimconstraint1 = ""
		aimconstraint2 = ""
		if ("_l_" in rotJnt) or ("_m_" in rotJnt):
			aimconstraint1 = cmds.aimConstraint(aimJnt, upperRotJnt, maintainOffset = False, worldUpType = "objectrotation", 
				worldUpObject = "anim_spine_lipWorldUp", worldUpVector = [0, -1, 0], aimVector = [0, 1, 0])
			aimconstraint2 = cmds.aimConstraint(aimJnt, lowerRotJnt, maintainOffset = False, worldUpType = "objectrotation", 
				worldUpObject = "anim_spine_lipWorldUp", worldUpVector = [0, -1, 0], aimVector = [0, 1, 0])
		else:
			aimconstraint1 = cmds.aimConstraint(aimJnt, upperRotJnt, maintainOffset = False, worldUpType = "objectrotation", 
				worldUpObject = "anim_spine_lipWorldUp", worldUpVector = [0, 1, 0], aimVector = [0, -1, 0])
			aimconstraint2 = cmds.aimConstraint(aimJnt, lowerRotJnt, maintainOffset = False, worldUpType = "objectrotation", 
				worldUpObject = "anim_spine_lipWorldUp", worldUpVector = [0, 1, 0], aimVector = [0, -1, 0])
		cmds.delete(aimconstraint1)
		cmds.delete(aimconstraint2)
		cmds.makeIdentity(rotJnt, rotate = True)
		if ("_l_" in rotJnt) or ("_m_" in rotJnt):
			aimconstraint = cmds.aimConstraint(aimJnt, rotJnt, maintainOffset = False, worldUpType = "objectrotation", 
				worldUpObject = "anim_spine_lipWorldUp", worldUpVector = [0, -1, 0], aimVector = [0, 1, 0])
		else:
			aimconstraint = cmds.aimConstraint(aimJnt, rotJnt, maintainOffset = False, worldUpType = "objectrotation", 
				worldUpObject = "anim_spine_lipWorldUp", worldUpVector = [0, 1, 0], aimVector = [0, -1, 0])
		cmds.parentConstraint(rotJnt, refJnt, maintainOffset = True)
addAimConstraints(cmds.ls(selection = True))