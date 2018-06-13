import maya.cmds as cmds
import string
def getMainName(name, prefix):
	mainName = name[len(prefix):]
	print "main name is" + mainName
	return mainName

# input all the ctrls that want enforce parent constraint on
def addParentConstraint(parentLs, childLs):
	if len(parentLs) != len(childLs):
		print "number of parents is not equal to number of children"
		return None
	for i in xrange(len(parentLs)):
		cmds.parentConstraint(parentLs[i], childLs[i], maintainOffset = True)


def addFkParentConstraint(ctrlLs):
	jntLs = []
	for ctrl in ctrlLs:
		jntName = string.replace("fk_" + getMainName(ctrl, "ctrl_") + "_jnt", "_fk", "")
		jntLs += [jntName]
	addParentConstraint(ctrlLs, jntLs)
addFkParentConstraint(cmds.ls(selection = True))