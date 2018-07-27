import maya.cmds as cmds
IKARMCTRLCHAIN = ["ctrl_l_ik_elbow" ,"ctrl_l_ik_wrist"]
FKARMCTRLCHAIN = ["ctrl_l_fk_shoulder" ,"ctrl_l_fk_elbow" ,"ctrl_l_fk_wrist"]
IKARMCTRLCHAIN_R = ["ctrl_r_ik_elbow" ,"ctrl_r_ik_wrist"]
FKARMCTRLCHAIN_R = ["ctrl_r_fk_shoulder" ,"ctrl_r_fk_elbow" ,"ctrl_r_fk_wrist"]
LEGFKCTRLCHAIN = ["ctrl_l_fk_femur" ,"ctrl_l_fk_knee" ,"ctrl_l_fk_ankle"]
LEGIKCTRLCHAIN = ["ctrl_l_knee" ,"ctrl_l_ik_foot"]
LEGFKCTRLCHAIN_R = ["ctrl_r_fk_femur" ,"ctrl_r_fk_knee" ,"ctrl_r_fk_ankle"]
LEGIKCTRLCHAIN_R = ["ctrl_r_knee" ,"ctrl_r_ik_foot"]
LEGSWITCHCTRL_R = "ctrl_r_legSwitch"
REVLEGNODE_R = "rev_r_leg"

# input: reverse node that's used in fk/ik switch; the ctrl and its attribute name for fk/ik switch
# fk chain, ik chain
# output: None
# side effects: add controls visibility to the fk/ik switch system
def connectVis(revNode, ctrlAttr, IkCtrlLs, FkCtrlLs):
	for i in xrange(len(IkCtrlLs)):
		cmds.connectAttr(ctrlAttr, IkCtrlLs[i] + ".visibility")
	for i in xrange(len(FkCtrlLs)):
		cmds.connectAttr(revNode + ".outputX", FkCtrlLs[i] + ".visibility")

def connectVis_UI(part):
	if part == "left arm":
		connectVis("rev_l_arm", "ctrl_l_armSwitch.ik_arm", IKARMCTRLCHAIN, FKARMCTRLCHAIN)
	elif part == "right arm":
		connectVis("rev_r_arm", "ctrl_r_armSwitch.ik_arm", IKARMCTRLCHAIN_R, FKARMCTRLCHAIN_R)
	elif part == "left leg":
		connectVis("rev_l_leg", "ctrl_l_legSwitch.ik_arm", IKARMCTRLCHAIN_R, FKARMCTRLCHAIN_R)
	elif part == "right leg":
		connectVis("rev_r_")
# LEFT
connectVis("rev_l_arm", "ctrl_l_armSwitch.ik_arm", IKARMCTRLCHAIN, FKARMCTRLCHAIN)
# right
connectVis("rev_r_arm", "ctrl_r_armSwitch.ik_arm", IKARMCTRLCHAIN_R, FKARMCTRLCHAIN_R)