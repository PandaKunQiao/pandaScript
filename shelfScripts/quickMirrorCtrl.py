import maya.cmds as cmds
import string

# function to get the new name from old name
# the duplicated 1 will be taken care of
# if the suffix is not 1, then it will let the suffix -1 and 
# get back to the original name for the new node

def getNewName(inputName, old, new):
	print inputName[-1]
	if inputName[-1] == "1":
		newName = string.replace(inputName[:-1], old, new)
	else:
		oldDigit = int(inputName[-1])
		newDigit = oldDigit -1
		newName = string.replace(inputName[:-1] + str(newDigit), old, new)
	return newName



controlTargets = cmds.ls(selection = True)
dupCtrllList = []
parentList = []
firstTrans = controlTargets[0]

# determine the direction
old = "_l_"
new = "_r_"
if "_r_" in firstTrans:
	old = "_r_"
	new = "_l_"

# duplicate each target, rename them and copy them to the list and group them
cmds.select(clear = True)
groupNode = cmds.createNode("transform", name = "temp_mirror_trans")
for transNode in controlTargets:

	# duplicate obj
	dupCtrlList = cmds.duplicate(transNode, renameChildren = True)

	# record the selected node first and rename it
	dupCtrlParent = dupCtrlList[0]
	newParentName = getNewName(dupCtrlParent, old, new)
	newDupCtrlParent = cmds.rename(dupCtrlParent, newParentName)
	# rename children of duplicated obj
	for dupCtrl in dupCtrlList[1:]:
		newName = getNewName(dupCtrl, old, new)
		newDupCtrl = cmds.rename(dupCtrl, newName)

	cmds.parent(newDupCtrlParent, groupNode)
	dupCtrllList += [newDupCtrlParent]

#mirror them over
cmds.setAttr(groupNode + ".scaleX", -1)
cmds.parent(dupCtrllList, world = True)
cmds.delete(groupNode)


