import maya.cmds as cmds


# STRETCHATTR = "ctrl_ik_r_wrist.stretchy_arm" 
# IKATTR = "ctrl_r_arm_switch.ik_arm" 
# VOLUMEATTR = "ctrl_ik_r_wrist.volume_preservation"
# SCALEATTR = "ctrl_apple.global_scale"
# DISTLABLE = "r_stretchy_arm"


# # query for objects
# objList = cmds.ls(selection = True)
# objList = ["bn_r_shoulder", "ctrl_ik_r_wrist", "bn_r_elbow", 
# 		   "ik_r_shoulder", "ik_r_elbow", 
# 		   "twist_r_shoulder_1", "twist_r_shoulder_2", "twist_r_shoulder_3", 
# 		   "twist_r_shoulder_start", "twist_r_shoulder_end", 
# 		   "nonRot_r_shoulder_start", "nonRot_r_elbow_start",
# 		   "twist_r_elbow_1", "twist_r_elbow_2", "twist_r_elbow_3", 
# 		   "twist_r_elbow_start", "twist_r_elbow_end"]


# STRETCHATTR = "ctrl_ik_r_foot.stretchy_leg" 
# IKATTR = "ctrl_r_leg_fkik.ik_leg" 
# VOLUMEATTR = "ctrl_ik_r_foot.volume_preservation"
# SCALEATTR = "ctrl_apple.global_scale"
# DISTLABLE = "r_stretchy_leg"


# # query for objects
# objList = cmds.ls(selection = True)
# objList = ["bn_r_femur", "ctrl_ik_r_foot", "bn_r_knee", 
# 		   "ik_r_femur", "ik_r_knee", 
# 		   "twist_r_femur_1", "twist_r_femur_2", "twist_r_femur_3", 
# 		   "twist_r_femur_start", "twist_r_femur_end", 
# 		   "nonRot_r_femur_start", "nonRot_r_knee_start",
# 		   "twist_r_knee_1", "twist_r_knee_2", "twist_r_knee_3", 
# 		   "twist_r_knee_start", "twist_r_knee_end"]


STRETCHATTR = "ctrl_ik_l_foot.stretchy_leg" 
IKATTR = "ctrl_l_leg_fkik.ik_leg" 
VOLUMEATTR = "ctrl_ik_l_foot.volume_preservation"
SCALEATTR = "ctrl_apple.global_scale"
DISTLABLE = "l_stretchy_leg"


# query for objects
objList = cmds.ls(selection = True)
objList = ["bn_l_femur", "ctrl_ik_l_foot", "bn_l_knee", 
		   "ik_l_femur", "ik_l_knee", 
		   "twist_l_femur_1", "twist_l_femur_2", "twist_l_femur_3", 
		   "twist_l_femur_start", "twist_l_femur_end", 
		   "nonRot_l_femur_start", "nonRot_l_knee_start",
		   "twist_l_knee_1", "twist_l_knee_2", "twist_l_knee_3", 
		   "twist_l_knee_start", "twist_l_knee_end"]

# start and end points
startObject = objList[0]
endObject = objList[1]


# joints to be influcenced
jointList = objList[2:] + [startObject]


# create locators
startLoc = cmds.spaceLocator(name = startObject + "_start_loc")[0]
endLoc = cmds.spaceLocator(name = endObject + "_end_loc")[0]


# get names of shape nodes
startLocShape = startLoc + "Shape"
endLocShape = endLoc + "Shape"


# constraint locators to objects
startPointCons = cmds.pointConstraint(startObject, startLoc)
cmds.delete(startPointCons)
endPointCons = cmds.pointConstraint(endObject, endLoc)


# create distance node and connect start and end
distanceNode = cmds.createNode("distanceDimShape")
distanceTrans = cmds.listRelatives(parent = True)[0]
distanceTrans = cmds.rename(distanceTrans, "dist_" + DISTLABLE)
distanceNode = distanceTrans + "Shape"
cmds.connectAttr(startLocShape + ".worldPosition[0]", 
	distanceNode + ".startPoint")
cmds.connectAttr(endLocShape + ".worldPosition[0]", distanceNode + ".endPoint")
origDist = cmds.getAttr(distanceNode + ".distance")


# create utility nodes and do the math
# output = dist/(origDist * global_scale)
divNode = cmds.createNode("multiplyDivide", name = "div_" + distanceTrans)
cmds.setAttr(divNode + ".operation", 2)
normNode = cmds.createNode("multiplyDivide", name = "norm_" + distanceTrans)
cmds.setAttr(normNode + ".operation", 1)
cmds.setAttr(normNode + ".input2X", origDist)
cmds.connectAttr(SCALEATTR, normNode + ".input1X")
cmds.connectAttr(distanceNode + ".distance", divNode + ".input1X")
cmds.connectAttr(normNode + ".outputX", divNode + ".input2X")

# create utility nodes for adding switch
colorBlendNode = cmds.createNode("blendColors", 
					name = "bc_stretchy_" + distanceTrans)
cmds.connectAttr(STRETCHATTR, colorBlendNode + ".blender")
cmds.connectAttr(divNode + ".output", colorBlendNode + ".color1")
cmds.setAttr(colorBlendNode + ".color2R", 1)
cmds.setAttr(colorBlendNode + ".color2G", 1)
cmds.setAttr(colorBlendNode + ".color2B", 1)


# utility nodes for conditions
condNode = cmds.createNode("condition", name = "cond_" + distanceTrans)
cmds.connectAttr(distanceNode + ".distance", condNode + ".firstTerm")
cmds.connectAttr(normNode + ".outputX", condNode + ".secondTerm")
cmds.setAttr(condNode + ".operation", 2)
cmds.connectAttr(colorBlendNode + ".output", condNode + ".colorIfTrue")
cmds.setAttr(condNode + ".colorIfFalseR", 1)
cmds.setAttr(condNode + ".colorIfFalseG", 1)
cmds.setAttr(condNode + ".colorIfFalseB", 1)


# utility nodes for volume preservation
# scale Y, scaleZ = (conditioned output)^(-1 + offset)
powNode = cmds.createNode("multiplyDivide", name = "pow_" + distanceTrans)
cmds.setAttr(powNode + ".operation", 3)
offsetNode = cmds.createNode("plusMinusAverage", name = "plus_"+ distanceTrans)
cmds.setAttr(offsetNode + ".input1D[0]", -1)
cmds.setAttr(offsetNode + ".operation", 1)
cmds.connectAttr(VOLUMEATTR, offsetNode + ".input1D[1]")
cmds.connectAttr(condNode + ".outColorR", powNode + ".input1X")
cmds.connectAttr(offsetNode + ".output1D", powNode + ".input2X")


# create utility nodes for linking them to ik switch
colorBlendIKNode = cmds.createNode("blendColors", 
						name = "bc_ikStretchy_" + distanceTrans)
cmds.connectAttr(IKATTR, colorBlendIKNode + ".blender")
cmds.connectAttr(condNode + ".outColor", colorBlendIKNode + ".color1")
cmds.setAttr(colorBlendIKNode + ".color2R", 1)
cmds.setAttr(colorBlendIKNode + ".color2G", 1)
cmds.setAttr(colorBlendIKNode + ".color2B", 1)


# connect scale attributes to the divided result
for joint in jointList:
 	cmds.connectAttr(colorBlendIKNode + ".outputR", joint + ".scaleX")
 	cmds.connectAttr(powNode + ".outputX", joint + ".scaleY")
 	cmds.connectAttr(powNode + ".outputX", joint + ".scaleZ")
