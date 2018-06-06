# function to copy the nurb into library
def storeCVInfo():
	nurbList = cmds.ls(selection = True)
	nurbInfoList = []
	for eachNurb in nurbList:
		cvPosList = []
		dupNurb = cmds.duplicate(eachNurb)[0]
		if cmds.listRelatives(eachNurb, parent = True) != None:
			cmds.parent(dupNurb, world = True)

		# put it back to 0 position
		cmds.setAttr(dupNurb + ".translateX", 0)
		cmds.setAttr(dupNurb + ".translateY", 0)
		cmds.setAttr(dupNurb + ".translateZ", 0)
		cmds.setAttr(dupNurb + ".rotateX", 0)
		cmds.setAttr(dupNurb + ".rotateY", 0)
		cmds.setAttr(dupNurb + ".rotateZ", 0)
		cmds.setAttr(dupNurb + ".scaleX", 0)
		cmds.setAttr(dupNurb + ".scaleY", 0)
		cmds.setAttr(dupNurb + ".scaleZ", 0)

		# read cvs
		numCV = cmds.getAttr(dupNurb+".spans")+cmds.getAttr(dupNurb+".degree")
		for i in xrange(numCV):
			cvName = dupNurb + ".cv[" + str(i) + "]"
			rawPos = cmds.xform(cvName, query = True, 
								worldSpace = True, translation = True)
			for j in xrange(3):
				rawPos[j] = rawPos[j] * 10**12
			cvPosList += [tuple(rawPos)]
		nurbInfoList += [cvPosList]
	cmds.delete(dupNurb)
	return nurbInfoList

def printCVInfo(nurbInfoList, nameList = None):
	i = 0
	for eachCVList in nurbInfoList:
		printedString = ""

		# if name list is given, then assign them to variables 
		if nameList != None:
			printedString += (nameList[i] + " = ")

		# store information as a list of tuples: (float, float, float)
		printedString += "["
		for eachCV in eachCVList:

			# each printed should be a tuple, printed as (tansX, transY, transZ)
			printedString += ("(" + str(eachCV[0]) + ", ")
			printedString += (str(eachCV[1]) + ", ")
			printedString += (str(eachCV[2]) + "), ")

		# get rid of the last 2 chars ", " and add the "]"
		printedString = printedString[:-2] + "]"
		i += 1
		print printedString

def createNurb(posList, degree = 1, name = None):
	knotList = range(len(posList))
	if name == None:
		cmds.curve(point = posList, degree = 1, knot = knotList)



nurbInfoList = storeCVInfo()
printCVInfo(posList, ["circleX"])
createNurb(nurbInfoList[0])







