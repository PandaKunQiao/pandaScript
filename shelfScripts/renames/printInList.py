import maya.cmds as cmds

def printInList(chosenObj):
	wholeString = "["
	for i in xrange(len(chosenObj)):
		wholeString += '"'
		wholeString += chosenObj[i]
		wholeString += '"'
		wholeString += " ,"
	wholeString = wholeString[:-2]
	wholeString 
	wholeString += "]"
	print wholeString
printInList(cmds.ls(selection = True))