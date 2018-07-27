import maya.cmds as cmds
import string
BSPRE = "bsPose"
def conCorrectiveShapes(bsNode):
	weightLs = cmds.listAttr(bsNode, multi = True)
	for weight in weightLs:
		if (weight[0:6] == "bsPose" and (not cmds.connectionInfo(bsNode + "." + weight, isDestination = True))):
			maxValIndex = string.rfind(weight, "_")
			maxVal = weight[maxValIndex+1:]
			if maxVal[0] == "n":
				maxVal = -float(maxVal[1:])
			else:
				maxVal = float(maxVal)
			axisIndex = string.rfind(weight[:maxValIndex], "_")
			axis = weight[axisIndex+1]
			driverIndex = string.rfind(weight[:axisIndex], "_")

			# case that there is l or r in the driver's name
			sideIndex = string.rfind(weight[:driverIndex], "_")
			if (weight[sideIndex+1] == "l" or weight[sideIndex+1] == "r"):
				driver = "sk_" + weight[sideIndex+1:axisIndex] + "_jnt"
			else:
				driver = "sk_" + weight[driverIndex+1:axisIndex] + "_jnt"
			cmds.setDrivenKeyframe(bsNode + "." + weight, cd = driver + ".rotate" + string.upper(axis), driverValue = 0, value = 0, itt = "linear", ott = "linear")
			cmds.setDrivenKeyframe(bsNode + "." + weight, cd = driver + ".rotate" + string.upper(axis), driverValue = maxVal, value = 1, itt = "linear", ott = "linear")

conCorrectiveShapes("bs_r_leg")