import maya.cmds as cmds
import string
BSPRE = "bsPose"
def conCorrectiveShapes(bsNode):
	weightLs = cmds.listAttr(bsNode, multi = True)
	for weight in weightLs:
		if (weight[0:6] == "bsPose" and (not cmds.connectionInfo(bsNode + "." + weight, isDestination = True))):
			newName = string.replace(string.replace(weight, "_l_", "_r_"), "_Copy", "")

			cmds.aliasAttr(newName, bsNode + "." + weight)
conCorrectiveShapes("bs_cloak")