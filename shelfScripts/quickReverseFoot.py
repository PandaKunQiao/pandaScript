import maya.cmds as cmds

# start with choosing the reverse foot skeleton structure
jntChain = cmds.ls(selection = True)
ATTRLS = [("custom_attributes", "enum", ("_________", 0)), 
		  ("foot_roll", "float", 0), 
		  ("heel_pivot", "float", 0), 
		  ("heel_slide", "float", 0), 
		  ("toe_pivot", "float", 0), 
		  ("toe_slide", "float", 0), 
		  ("ball_pivot", "float", 0), 
		  ("ball_slide", "float", 0),
		  ("banking", "float", 0)]

if jntChain[0][4] == "l":
	RFCHAIN = ["rf_l_outFoot_jnt", "rf_l_inFoot_jnt", "rf_l_heel_jnt", 
			   "rf_l_toe_jnt", "rf_l_ball_jnt", "rf_l_ankle_jnt"]
	RFCTRL = "ctrl_l_ik_foot"
else:
	RFCHAIN = ["rf_r_outFoot_jnt", "rf_r_inFoot_jnt", "rf_r_heel_jnt", 
			   "rf_r_toe_jnt", "rf_r_ball_jnt", "rf_r_ankle_jnt"]
	RFCTRL = "ctrl_r_ik_foot"

# function to add ikhandles to selected joints
# return a list of (ikhandle, effector)
def addIkChain(jntChain):
	numJnt = len(jntChain)
	rstLs = []
	for i in xrange(numJnt-1):
		startJnt = jntChain[i]
		endJnt = jntChain[i+1]
		ikHandleName = endJnt[:-3] + "ikHandle"
		handleEffLs = cmds.ikHandle(startJoint = startJnt, endEffector = endJnt, 
									solver = "ikRPsolver", name = ikHandleName)
		eff = handleEffLs[1]
		eff = cmds.rename(eff, endJnt[:-3] + "eff")
		handleJnt = (handleEffLs[0], eff)
		rstLs += handleJnt
	return rstLs

# add additional joint at ball, toe and ankle for foot roll and pivot, slide
def rfAddJnt():
	heelJnt = RFCHAIN[2]
	toeJnt = RFCHAIN[3]
	ballJnt = RFCHAIN[4]
	ankleJnt = RFCHAIN[5]
	refHeelJnt = cmds.rename(heelJnt, "footRoll_" + heelJnt)
	refToeJnt = cmds.rename(toeJnt, "footRoll_" + toeJnt)
	refBallJnt = cmds.rename(ballJnt, "footRoll_" + ballJnt)

	cmds.select(refBallJnt)
	childBall = cmds.joint(name = ballJnt)
	cmds.parent(ankleJnt, ballJnt)

	cmds.select(refToeJnt)
	childToe = cmds.joint(name = toeJnt)
	cmds.parent(refBallJnt, childToe)

	cmds.select(refHeelJnt)
	childHeel = cmds.joint(name = heelJnt)
	cmds.parent(refToeJnt, childHeel)

# add custom attributes to the control
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


# set up attributes for reverse foot, this function is hard-coded and only for 
# this specific input of names
def rigRf(jntLs, handleEffLs):

	# rig foot rolling
	cmds.setDrivenKeyframe(currentDriver = "nurbsCircle1.translateX", attribute = "pSphere.translateX", value = 1)


addIkChain(jntChain)
addAttrToCtrl(RFCTRL, ATTRLS)
rfAddJnt()