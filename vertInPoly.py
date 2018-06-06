import maya.cmds as cmds
from functools import partial
import maya.mel as mel
import math
import string
import copy
import numpy as np

# Choose adjacent poly library

# input: "POLY: num, num, num, num"
# output [num, num, num, num] (all nums are strings)
def infoToIndex(information):
	startIndex = string.find(information, ":") + 3
	return string.split(information[startIndex:])

# input: transform node's name, polytype, [index, index...]
# output: a list of poly names
def indexToPoly(transName, polyName, indexList):
	result = []
	for i in xrange(len(indexList)):
		result += [transName + "." + polyName + "[" + indexList[i] + "]"]
	return result

def polyToIndex(polyList):
	result = []
	for poly in polyList:
		index = string.find(poly, "[")
		result += [int(poly[index+1])]
	return result

# input: poly name
# output: transform node's name
def polyToTrans(poly):
	endIndex = string.find(poly, ".")
	return poly[:endIndex]


# input: vertex
# output: [face, face, face...]
def vertexToAdjacentFace(vertex):
	transName = polyToTrans(vertex)
	oldSelection = cmds.ls(selection = True)
	cmds.select(vertex)

	# the vertex must be selected, this function returns a string ["num1 num2 num3 num4"]
	indexString = cmds.polyInfo(vertexToFace = True)[0]
	cmds.select(oldSelection)
	indexList = infoToIndex(indexString)
	faceList = indexToPoly(transName, "f", indexList)
	return faceList

# input: face
# output: [vert, vert, vert...]
def faceToAdjacentVertex(face):
	oldSelection = cmds.ls(selection = True)
	transName = polyToTrans(face)
	cmds.select(face)
	indexString = cmds.polyInfo(faceToVertex = True)[0]
	cmds.select(oldSelection)
	indexList = infoToIndex(indexString)
	vertList = indexToPoly(transName, "vtx", indexList)
	return vertList


# input: vertex
# output: [vert, vert, vert...]
def vertexToAdjacentVertices(vertex):
	faceList = vertexToAdjacentFace(vertex)
	transName = polyToTrans(vertex)
	vertList = []
	for i in xrange(len(faceList)):
		vertList += faceToAdjacentVertex(faceList[i])
	# get rid of repetitive elements
	return list(set(vertList))

# input: face
# output: [face, face, face, ...]
def faceToAdjacentFaces(face):
	transName = polyToTrans(face)
	vertList = faceToAdjacentVertex(face)
	faceList = []
	for i in xrange(len(vertList)):
		faceList += vertexToAdjacentFace(vertList[i])
	# get rid of repetitive elements
	return list(set(faceList))

# all are the mult version of verts
def vertsToVerts(vertList):
	result = []
	for vert in vertList:
		result += vertexToAdjacentVertices(vert)
	return list(set(result))

def facesToFaces(faceList):
	result = []
	for face in faceList:
		result += faceToAdjacentFaces(face)
	return list(set(result))


def vertsToFaces(vertList):
	result = []
	for vert in vertList:
		result += vertexToAdjacentFace(vert)
	return list(set(result))

def faceToVerts(faceList):
	result = []
	for face in faceList:
		result += faceToAdjacentVertex(face)
	return list(set(result))




# end of library

def minusVerts(vert1, vert2):
	result = []
	if len(vert1) != len(vert2):
		print "minusVerts not same length"
		return None
	for i in xrange(len(vert1)):
		result += [vert1[i] - vert2[i]]
	return result

# lineFunc format: [[l, x1], [m, y1], [n, z1]]
class Line:
	def __init__(self, vert1, vert2):
		vec = minusVerts(vert1, vert2)
		lineFunc = []
		for i in xrange(len(vec)):
			lineFunc += [[vec[i], vert1[i]]]
		self.lineFunc = lineFunc
		self.l = vec[0]
		self.m = vec[1]
		self.n = vec[2]

		self.x = vert1[0]
		self.y = vert1[1]
		self.z = vert1[2]


	def getPointOnLine(self, value, axis):
		result = [0, 0, 0]
		if axis == "x":
			t = (value - self.lineFunc[0][1])/self.lineFunc[0][0]
			result[0] = value
			result[1] = t * self.lineFunc[1][0] + self.lineFunc[1][1]
			result[2] = t * self.lineFunc[2][0] + self.lineFunc[2][1]
		if axis == "y":
			t = (value - self.lineFunc[1][1])/self.lineFunc[1][0]
			result[1] = value
			result[0] = t * self.lineFunc[0][0] + self.lineFunc[0][1]
			result[2] = t * self.lineFunc[2][0] + self.lineFunc[2][1]
		if axis == "z":
			t = (value - self.lineFunc[2][1])/self.lineFunc[2][0]
			result[2] = value
			result[0] = t * self.lineFunc[0][0] + self.lineFunc[0][1]
			result[1] = t * self.lineFunc[1][0] + self.lineFunc[1][1]
		return result


	def leftOrRight(self, vertTest):
		pointOnLine = self.getPointOnLine(vertTest[2], "z")
		if vertTest[0] > pointOnLine[0]:
			return "R"
		else:
			return "L"


	def upOrDown(self, vertTest):
		pointOnLine = self.getPointOnLine(vertTest[0], "x")
		if vertTest[1] > pointOnLine[1]:
			return "U"
		else:
			return "D"

	def frontOrBack(self, vertTest):
		pointOnLine = self.getPointOnLine(vertTest[1], "y")
		if vertTest[2] > pointOnLine[2]:
			return "F"
		else:
			return "B"


# plane is an class with ax + by + cz = s
class Plane:

	# init function, starting from two lines
	def __init__(self, line1, line2):
		connectingLine = minusVerts([line2.x, line2.y, line2.z], [line1.x, line1.y, line1.z])
		crossProduct = np.cross(connectingLine, [line1.l, line1.m, line1.n])
		scalar = np.vdot (np.array(crossProduct), np.array([line2.x, line2.y, line2.z]))
		self.a = crossProduct[0]
		self.b = crossProduct[1]
		self.c = crossProduct[2]
		self.s = scalar

		# one arbitrary point on the plane
		self.point = [line1.x, line1.y, line1.z]


	# given 2 values, find the point on the plane
	def getPointOnPlane(self, value1, value2, axis):
		result = [0, 0, 0]
		if axis == "xy":
			result[0] = value1
			result[1] = value2
			result[2]= (self.s - self.a * value1 - self.b * value2)/self.c
		if axis == "yz":
			result[1] = value1
			result[2] = value2
			result[0]= (self.s - self.b * value1 - self.c * value2)/self.a
		if axis == "xz":
			result[0] = value1
			result[2] = value2
			result[1]= (self.s - self.a * value1 - self.c * value2)/self.b
		return result




	def leftOrRight(self, vertTest):
		pointOnPlane = self.getPointOnPlane(vertTest[1], vertTest[2], "yz")
		if vertTest[0] > pointOnPlane[0]:
			return "R"
		else:
			return "L"


	def frontOrBack(self, vertTest):
		pointOnPlane = self.getPointOnPlane(vertTest[0], vertTest[1], "xy")
		if vertTest[2] > pointOnPlane[2]:
			return "F"
		else:
			return "B"

	def upOrDown(self, vertTest):
		pointOnPlane = self.getPointOnPlane(vertTest[0], vertTest[2], "xz")
		if vertTest[1] > pointOnPlane[1]:
			return "U"
		else:
			return "D"

	def printVal(self):
		print self.a
		print "A: " + str(self.a)
		print "B: " + str(self.b)
		print "C: " + str(self.c)
		print "S: " + str(self.s)

# input: 2 planes and [x, y, z], 
# output if the vert is between the two plane
def inBetweenPlanes(plane1, plane2, vert):
	x = vert[0]
	y = vert[1]
	z = vert[2]

	px = plane2.point[0]
	py = plane2.point[1]
	pz = plane2.point[2]
	planeDist = (plane1.a * px) + (plane1.b * py) + (plane1.c * pz) + (-plane1.s)
	dotOne = (plane1.a * x) + (plane1.b * y) + (plane1.c * z) + (-plane1.s)

	# same sign, on the same side, different sign, on different sides
	return ((dotOne  * planeDist) > 0) and (abs(planeDist) > abs(dotOne))

def testPlaneAll(side, plane):
	print "test plane"
	selectionList = []
	plane.printVal()
	for i in xrange(288):
		cubeName = "pCube" + str(i+1)
		if (side == "U" or side == "D"):
			if plane.upOrDown(cmds.xform(cubeName, translation = True, worldSpace = True, query = True)) == side:
				selectionList += [cubeName]
		elif (side == "R" or side == "L"):
			if plane.leftOrRight(cmds.xform(cubeName, translation = True, worldSpace = True, query = True)) == side:
				selectionList += [cubeName]
		elif (side == "F" or side == "B"):
			if plane.frontOrBack(cmds.xform(cubeName, translation = True, worldSpace = True, query = True)) == side:
				selectionList += [cubeName]

	cmds.select(selectionList)


# the box is initiated by 3 pairs of planes, which are the faces of the boxes that oppsite with each other
class Box:
	def __init__(self, planeSet1, planeSet2, planeSet3, faceList, addType,
				 vertLTB, vertLTF, vertLBB, vertLBF, 
				 vertRTB, vertRTF, vertRBB, vertRBF):
		self.planeU = planeSet1[0]
		self.planeD = planeSet1[1]
		self.planeR = planeSet2[0]
		self.planeL = planeSet2[1]
		self.planeB = planeSet3[0]
		self.planeF = planeSet3[1]

		self.faceList = faceList
		self.vertList = faceToVerts(faceList)
		self.addType = addType

		# vertex order to compute the planes in the right order
		self.vertLTB = vertLTB
		self.vertLTF = vertLTF
		self.vertLBB = vertLBB
		self.vertLBF = vertLBF
		self.vertRTB = vertRTB
		self.vertRTF = vertRTF
		self.vertRBB = vertRBB
		self.vertRBF = vertRBF

	
	def checkFace(self, face):
		return (face in self.faceList)


	def insideBox(self, vertTest):
		if (inBetweenPlanes(self.planeU, self.planeD, vertTest) and
		    inBetweenPlanes(self.planeF, self.planeB, vertTest) and
		    inBetweenPlanes(self.planeL, self.planeR, vertTest)):
		# if (self.planeU.upOrDown(vertTest) != self.planeD.upOrDown(vertTest) and 
		# 	self.planeL.leftOrRight(vertTest) != self.planeR.leftOrRight(vertTest) and 
		# 	self.planeF.frontOrBack(vertTest) != self.planeB.frontOrBack(vertTest)):
			return True
		else:
			return False

	def updateMath(self):
		meshVertList = polyToIndex(self.vertList)
		print meshVertList
		mesh = polyToTrans(self.vertList[0])
		# sort positions of vertices in x, y and z directions

		# create box
		posList = [-1]
		posList += [cmds.xform(self.vertRTF, query = True, translation = True, worldSpace = True)]
		posList += [cmds.xform(self.vertRTB, query = True, translation = True, worldSpace = True)]
		posList += [cmds.xform(self.vertLTB, query = True, translation = True, worldSpace = True)]
		posList += [cmds.xform(self.vertLTF, query = True, translation = True, worldSpace = True)]
		posList += [cmds.xform(self.vertLBF, query = True, translation = True, worldSpace = True)]
		posList += [cmds.xform(self.vertLBB, query = True, translation = True, worldSpace = True)]
		posList += [cmds.xform(self.vertRBB, query = True, translation = True, worldSpace = True)]
		posList += [cmds.xform(self.vertRBF, query = True, translation = True, worldSpace = True)]
		print posList


		# up and down faces
		line1 = Line(posList[1], posList[2])
		line2 = Line(posList[3], posList[4])
		self.planeU = Plane(line1, line2)
		

		line3 = Line(posList[5], posList[6])
		line4 = Line(posList[7], posList[8])
		self.planeD = Plane(line3, line4)

		# left and right faces
		self.planeR = Plane(line1, line4)
		self.planeL = Plane(line2, line3)


		# front and back faces
		line5 = Line(posList[2], posList[3])
		line6 = Line(posList[6], posList[7])
		self.planeB = Plane(line5, line6)

		line7 = Line(posList[1], posList[4])
		line8 = Line(posList[5], posList[8])
		self.planeF = Plane(line7, line8)
		return None
	

	def printVal(self):
		print " "
		print "begin - box info:"
		print "U: "
		self.planeU.printVal()
		print "D:"
		self.planeD.printVal()
		print "R: "
		self.planeR.printVal()
		print "L: "
		self.planeL.printVal()
		print "B: "
		self.planeB.printVal()
		print "F: "
		self.planeB.printVal()
		print "end - boxinfo"
		print " "


# the function to create a box object from maya mesh
def createBox(mesh, meshVertList, meshFaceList, addType):
	print mesh
	print meshVertList
	print meshFaceList
	print addType

	# sort positions of vertices in x, y and z directions
	xList = copy.deepcopy(meshVertList)
	yList = copy.deepcopy(meshVertList)
	zList = copy.deepcopy(meshVertList)
	positionList = []
	for i in meshVertList:
		meshVert = mesh + ".vtx[" + str(i) + "]"
		xList[i] = (xList[i], cmds.xform(meshVert, query = True, translation = True))
		yList[i] = (yList[i], cmds.xform(meshVert, query = True, translation = True))
		zList[i] = (zList[i], cmds.xform(meshVert, query = True, translation = True))
	xList.sort(key=lambda x: x[1][0])
	yList.sort(key=lambda x: x[1][1])
	zList.sort(key=lambda x: x[1][2])
	print xList
	print yList
	print zList

	for i in meshVertList:
		meshVert = mesh + ".vtx[" + str(i) + "]"
		xList[i] = xList[i][0]
		yList[i] = yList[i][0]
		zList[i] = zList[i][0]
	# assign init value to 8 vertices of the box
	vertLTB = -1
	vertLTF = -1
	vertLBB = -1
	vertLBF	= -1
	vertRTB = -1
	vertRTF = -1
	vertRBB = -1
	vertRBF = -1

	# find position of each vertex
	for i in meshVertList:
		vertName = mesh+".vtx[" + str(i) + "]"
		if (i in xList[0:4]):
			if (i in yList[0:4]):
				if (i in zList[0:4]):
					vertLBB = vertName
				else:
					vertLBF = vertName
			else:
				if (i in zList[0:4]):
					vertLTB = vertName
				else:
					vertLTF = vertName
		else:
			if (i in yList[0:4]):
				if (i in zList[0:4]):
					vertRBB = vertName
				else:
					vertRBF = vertName
			else:
				if (i in zList[0:4]):
					vertRTB = vertName
				else:
					vertRTF = vertName

	# create box
	posList = [-1]
	posList += [cmds.xform(vertRTF, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertRTB, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertLTB, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertLTF, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertLBF, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertLBB, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertRBB, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertRBF, query = True, translation = True, worldSpace = True)]

	# up and down faces
	line1 = Line(posList[1], posList[2])
	line2 = Line(posList[3], posList[4])
	planeA1 = Plane(line1, line2)

	line3 = Line(posList[5], posList[6])
	line4 = Line(posList[7], posList[8])
	planeA2 = Plane(line3, line4)

	# left and right faces
	planeB1 = Plane(line1, line4)
	planeB2 = Plane(line2, line3)


	# front and back faces
	line5 = Line(posList[2], posList[3])
	line6 = Line(posList[6], posList[7])
	planeC1 = Plane(line5, line6)

	line7 = Line(posList[1], posList[4])
	line8 = Line(posList[5], posList[8])
	planeC2 = Plane(line7, line8)

	faceList = []
	for i in meshFaceList :
		faceList += [mesh + ".f[" + str(i) + "]"]

	return Box([planeA1, planeA2], [planeB1, planeB2], [planeC1, planeC2], 
				faceList, addType, 
				vertLTB, vertLTF, vertLBB, vertLBF, 
				vertRTB, vertRTF, vertRBB, vertRBF)

# the function to create a box from maya mesh
def getBoxFromView(addType = "additive"):
	mesh = cmds.ls(selection = True)[0]
	meshFaceList = range(8)
	meshVertList = range(8)
	return createBox(mesh, meshVertList, meshFaceList, addType)

def getBoxFromMesh(mesh, addType = "additive"):
	meshFaceList = range(8)
	meshVertList = range(8)
	return createBox(mesh, meshVertList, meshFaceList, addType)



# polygon object has 2 features, one is a dictionary, the other is the number of levels.
# poly is a type that interact with meshes
# Each polygon is eather a plane or another polygon
class Poly:
	def __init__(self, box):
		# The list of boxes
		self.boxList = [box]
		faceList = box.faceList
		meshName = polyToTrans(faceList[0])
		# dictionary of boxes, keys are mesh names
		self.boxDict = dict([])
		self.boxDict[meshName] = box
		# number of boxes in poly
		self.boxNum = 1

	# first iterate through all levels, and check each box's inside objects.
	# vert lists are the string names
	# If they are in the previous ones, delete them, if not, add them
	def insidePoly(self, vertList):
		chosenVertList = []
		boxList = self.boxList
		# print vertList
		for meshVert in vertList:
			vert = cmds.xform(meshVert, query = True, translation = True, worldSpace = True)
			record = False
			for i in xrange(len(boxList)):
				box = boxList[i]
				# print "before call insidebox"
				if box.insideBox(vert):
					# print "success call insidebox"
					# print box.addType
					if box.addType == "additive":
						record = True
					else:
						record = False
					# print record
			if record:
				chosenVertList += [meshVert]
		return chosenVertList

	# given the extended face and the new face list, update the poly with
	# new box
	def addBox(self, mesh, box):
		self.boxDict[mesh] = box
		self.boxList += [box]
		self.boxNum += 1
		# update the old box attributes


	# given the faceList, update the polygon's box whose keys are the faces in the list
	def updateBox(self, mesh):
		box = self.boxDict[mesh]
		box.updateMath()

# wrapper function to create poly from selection
def getPolyFromView():
	mesh = cmds.ls(selection = True)[0]
	meshFaceList = range(8)
	meshVertList = range(8)
	box = createBox(mesh, meshVertList, meshFaceList, "additive")
	return Poly(box)

# wrapper function to create poly from a mesh name
def getPolyFromMesh(mesh):
	meshFaceList = range(8)
	meshVertList = range(8)
	box = createBox(mesh, meshVertList, meshFaceList, "additive")
	return Poly(box)




# user interface


# get vertices
def getVerts(fakeInput, vertList):
	oldSelection = cmds.ls(selection = True)
	del vertList[:]
	objList = cmds.ls(selection = True, flatten = True)
	for obj in objList:
		cmds.select(obj)
		numVert = cmds.polyEvaluate(vertex = True)
		for i in xrange(numVert):
			vertList += [obj + ".vtx[" + str(i) + "]"]
	cmds.select(oldSelection)
	print len(vertList)

# put the type list into container
def fillBoxType(item, typeList):
	typeList[0] = item

# change the existedTypeList according to new option menu item
def changeTypeList(item, meshName, existedTypeList):
	index = int(meshName[-1])
	existedTypeList[index] = item

# wrapper to choose mesh
def chooseMesh(fakeInput, meshName):
	cmds.select(meshName)

# The function is called when user hit the button "refresh". The chosen mesh box's position will
# be updated and verts will be selected according to the new box's position and their new addtype
def refresh(fakeInput, vertList, polyList, existedTypeList):
	poly = polyList[0]
	for i in xrange(poly.boxNum):
		box = poly.boxList[i]
		box.addType = existedTypeList[i]
		box.updateMath()
		if existedTypeList[i] == "additive":
			cmds.setAttr("pandaCube" + str(i) + ".overrideColor", 13)
		else:
			cmds.setAttr("pandaCube" + str(i) + ".overrideColor", 6)
	chosenVertList = poly.insidePoly(vertList)
	cmds.select(poly.insidePoly(vertList))

# When creating box, the option menu start from addtive
def menuOrderAdd():
	cmds.menuItem(label = "additive")
	cmds.menuItem(label = "subtractive")

# When creating box, the option menu start from subtractive
def menuOrderSub():
	cmds.menuItem(label = "subtractive")
	cmds.menuItem(label = "additive")

# Function to add group at layout
def addRowGroup(meshName, layoutName, existedTypeList, typeList):
	cmds.rowLayout( numberOfColumns=3, 
					columnAttach=[(1, 'both', 10), (2, "both", 10), (3, "both", 10)],
					columnWidth=[(1, 200), (2, 150), (3, 150)],
					height = 50, parent = layoutName)
	cmds.optionMenu(label = "box type",
					changeCommand = partial(changeTypeList, meshName = meshName, 
															existedTypeList = existedTypeList,
															))
	if typeList[0] == "additive":
		menuOrderAdd()
	else:
		menuOrderSub()
	cmds.text(label = meshName)
	cmds.button(label = "select", command = partial(chooseMesh, meshName = meshName))



# The function is called when user hit the button "create", if no box existed, create a poly
# if there is already a poly and boxes, add one more box to the poly
def create(fakeInput, vertList, polyList, typeList, layoutName, existedTypeList):
	if polyList == []:
		meshCube = cmds.polyCube(name = "pandaCube0")[0]
		poly = getPolyFromMesh(meshCube)
		polyList += [poly]
	else:
		poly = polyList[0]
		meshCube = cmds.polyCube(name = "pandaCube" + str(poly.boxNum))[0]
		box = getBoxFromMesh(meshCube, addType = typeList[0])
		poly.addBox(meshCube, box)

	cmds.setAttr(meshCube + ".overrideEnabled", 1)
	cmds.setAttr(meshCube + ".overrideShading", 0)
	if typeList[0] == "additive":
		cmds.setAttr(meshCube + ".overrideColor", 13)
	else:
		cmds.setAttr(meshCube + ".overrideColor", 6)


	existedTypeList += [typeList[0]]
	chosenVertList = poly.insidePoly(vertList)
	cmds.select(poly.insidePoly(vertList))
	addRowGroup(meshCube, layoutName, existedTypeList, typeList)


# Function to delete clear the boxes
def delete(fakeInput, polyList):
	poly = polyList[0]
	for i in xrange(poly.boxNum):
		cmds.delete("pandaCube" + str(i))

# The real UI function
def win(fakeInput = True):
	win_Name = "PandaMenu 3D Choose Tool"
	versionNumber = 0.1

	#if old ui not closed, close it
	if cmds.window(win_Name, exists = True):
		cmds.deleteUI(win_Name)
	window = cmds.window(win_Name, sizeable = True,
							titleBar = True, resizeToFitChildren = False,
							menuBar = True,
							title = win_Name + " ver " + str(versionNumber))

	#global list that contains cross-window selection names
	vertList = []
	polyList = []
	typeList = ["additive"]
	existedTypeList = []



	#col layout
	cmds.columnLayout()

	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=(1, 'both', 135), 
					columnWidth=(1, 250),
					height = 50 )
	cmds.button( label='Confirm Objects need to be chosen', 
				 command = partial(getVerts, vertList = vertList), 
				 width = 250)
	cmds.setParent("..")


	addRowLayout = cmds.columnLayout()
	cmds.setParent("..")
	


	cmds.rowLayout( numberOfColumns=3, 
					columnAttach=[(1, 'both', 10), (2, "both", 10), (3, "both", 10)],
					columnWidth=[(1, 200), (2, 150), (3, 150)],
					height = 50)

	cmds.optionMenu( label='box type', 
					 changeCommand = partial(fillBoxType, typeList = typeList))
	cmds.menuItem(label = "additive")
	cmds.menuItem(label = "subtractive")

	cmds.button( label = 'Create Box', 
				 command = partial(create, vertList = vertList, 
				 						   polyList = polyList, 
				 						   typeList = typeList,
				 						   layoutName = addRowLayout,
				 						   existedTypeList = existedTypeList))
	cmds.button( label = "Refresh", command = partial(refresh, 
														  vertList = vertList,
														  polyList = polyList,
														  existedTypeList = existedTypeList))
	cmds.setParent("..")
	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=(1, 'both', 135), 
					columnWidth=(1, 250),
					height = 50 )
	cmds.button( label='Delete All Boxes', 
				 command = partial(delete, polyList = polyList), 
				 width = 250)
	cmds.setParent("..")
	cmds.showWindow( window )


# test functions for lines
def getLinePos():
	crv = cmds.ls(selection = True)[0]
	pos1 = cmds.xform(crv+".cv[0]", query = True, translation = True, worldSpace = True)
	pos2 = cmds.xform(crv+".cv[1]", query = True, translation = True, worldSpace = True)
	return [pos1, pos2]


def testLR(side):
	selectionList = []
	for i in xrange(288):
		cubeName = "pCube" + str(i+1)
		line = Line(vertList[0], vertList[1])
		if line.leftOrRight(cmds.xform(cubeName, translation = True, worldSpace = True, query = True)) == side:
			selectionList += [cubeName]
	cmds.select(selectionList)

def testUD(side):
	selectionList = []
	for i in xrange(288):
		cubeName = "pCube" + str(i+1)
		line = Line(vertList[0], vertList[1])
		if line.upOrDown(cmds.xform(cubeName, translation = True, worldSpace = True, query = True)) == side:
			selectionList += [cubeName]
	cmds.select(selectionList)

def testFB(side):
	selectionList = []
	for i in xrange(288):
		cubeName = "pCube" + str(i+1)
		line = Line(vertList[0], vertList[1])
		if line.frontOrBack(cmds.xform(cubeName, translation = True, worldSpace = True, query = True)) == side:
			selectionList += [cubeName]
	cmds.select(selectionList)

def getPlaneFromView():
	crv = cmds.ls(selection = True)[0]
	pos1 = cmds.xform(crv+".cv[0]", query = True, translation = True, worldSpace = True)
	pos2 = cmds.xform(crv+".cv[1]", query = True, translation = True, worldSpace = True)
	line1 = Line(pos1, pos2)

	pos3 = cmds.xform(crv+".cv[2]", query = True, translation = True, worldSpace = True)
	pos4 = cmds.xform(crv+".cv[3]", query = True, translation = True, worldSpace = True)
	line2 = Line(pos3, pos4)

	plane = Plane(line1, line2)
	plane.printVal
	return plane



def testUDPlaneOne(side):
	selectionList = []
	plane = getPlaneFromView()
	plane.printVal()
	cubeName = "pCube289"
	result = plane.upOrDown(cmds.xform(cubeName, translation = True, worldSpace = True, query = True))
	print result
	if  result == side:
		cmds.select(selectionList)



def testBoxAll(box):
	selectionList = []
	for i in xrange(288):
		cubeName = "pCube" + str(i+1)
		if box.insideBox(cmds.xform(cubeName, translation = True, worldSpace = True, query = True)):
			selectionList += [cubeName]
	cmds.select(selectionList)

def testBoxOne(box):
	selectionList = []
	cubeName = "pCube289"
	if box.insideBox(cmds.xform(cubeName, translation = True, worldSpace = True, query = True)):
		selectionList += [cubeName]

def testPolyAll(poly):
	selectionList = []
	box = getBoxFromView()
	for i in xrange(288):
		cubeName = "pCube" + str(i+1)
		if box.insideBox(cmds.xform(cubeName, translation = True, worldSpace = True, query = True)):
			selectionList += [cubeName]
	cmds.select(selectionList)
win()