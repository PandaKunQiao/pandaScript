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



# the box is initiated by 3 pairs of planes, which are the faces of the boxes that oppsite with each other
# The box class directly interact with mathmatical verts, instead of mesh names
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


	# take in a vert (x, y, z), return whether the vert is inside the box
	def insideBox(self, vertTest):
		if (inBetweenPlanes(self.planeU, self.planeD, vertTest) and
		    inBetweenPlanes(self.planeF, self.planeB, vertTest) and
		    inBetweenPlanes(self.planeL, self.planeR, vertTest)):
			return True
		else:
			return False

	# update the mathematical expression of each plane according to the mesh
	def updateMath(self):
		meshVertList = polyToIndex(self.vertList)
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

	# take a list of a vert list, each vert is a vector
	def filterInsideBox(self, vertList):
		result = []
		for vert in vertList:
			if self.insideBox(vert):
				result += [vert]
		return result
	

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




# user interface


# input: (mesh, empty list)
# side effect: input the empty list with vertices of the mesh
# output: None
def getVertsFromMesh(meshList, vertList):
	del vertList[:]
	objList = meshList 
	for obj in objList:
		cmds.select(obj)
		numVert = cmds.polyEvaluate(vertex = True)
		for i in xrange(numVert):
			vertList += [obj + ".vtx[" + str(i) + "]"]

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



# Part to create joints

def calcAngle(pos1, pos2, direction = "a"):
	# temp_loc = cmds.spaceLocator("loc_temp_angle")
	new_pos = [pos1[0]+1, pos1[1], pos1[2]]
	a = cmds.spaceLocator()
	cmds.xform(a, translation = new_pos)
	# cmds.xform(temp_loc, translation = new_pos)
	temp_vec_1 = cmds.createNode("plusMinusAverage")
	cmds.setAttr(temp_vec_1 + ".operation", 2)
	cmds.setAttr(temp_vec_1+".input3D[0].input3Dx", new_pos[0])
	cmds.setAttr(temp_vec_1+".input3D[0].input3Dy", new_pos[1])
	cmds.setAttr(temp_vec_1+".input3D[0].input3Dz", new_pos[2])
	cmds.setAttr(temp_vec_1+".input3D[1].input3Dx", pos1[0])
	cmds.setAttr(temp_vec_1+".input3D[1].input3Dy", pos1[1])
	cmds.setAttr(temp_vec_1+".input3D[1].input3Dz", pos1[2])

	temp_vec_2 = cmds.createNode("plusMinusAverage")
	cmds.setAttr(temp_vec_2 + ".operation", 2)
	cmds.setAttr(temp_vec_2+".input3D[0].input3Dx", pos2[0])
	cmds.setAttr(temp_vec_2+".input3D[0].input3Dy", pos2[1])
	cmds.setAttr(temp_vec_2+".input3D[0].input3Dz", pos2[2])
	cmds.setAttr(temp_vec_2+".input3D[1].input3Dx", pos1[0])
	cmds.setAttr(temp_vec_2+".input3D[1].input3Dy", pos1[1])
	cmds.setAttr(temp_vec_2+".input3D[1].input3Dz", pos1[2])

	temp_angle = cmds.createNode("angleBetween")
	cmds.connectAttr(temp_vec_1 + ".output3D", temp_angle + ".vector1")
	cmds.connectAttr(temp_vec_2 + ".output3D", temp_angle + ".vector2")
	return cmds.getAttr(temp_angle + ".euler")[0]
	return [temp_vec_1, temp_vec_2, temp_angle]

# given angle and position and the index, 
# create a shoulder joint and return its name
# name convention: armJnt_temp_
def createJoint(pos, angle, num):
	shoulderJoint = cmds.joint(name = "armJnt_temp_" + str(num))
	cmds.select([])
	cmds.xform(shoulderJoint, translation = pos, rotation = angle)
	return shoulderJoint


# helper function to create the joint chain
def createJointChain(posShoulder, posElbow, posWrist):
	shoulderAngle = calcAngle(posShoulder, posElbow)

	# create shoulder joint
	shoulderJnt = createJoint(posShoulder, shoulderAngle, 1)

	# create elbow joint, parent it under the shoulder
	elbowJoint = createJoint(posElbow, [0, 0, 0], 2)
	cmds.parent(elbowJoint, shoulderJnt)
	cmds.select([])

	# create wrist joint, parent it under the elbow
	wristJoint = createJoint(posWrist, [0, 0, 0], 3)
	cmds.parent(wristJoint, elbowJoint)
	cmds.select([])

	# temporily orient the joint back to 0 to orient joint
	cmds.xform(shoulderJnt, rotation = [0, 0, 0])
	cmds.select(shoulderJnt)
	cmds.joint(edit = True, orientJoint = "xzy", 
							secondaryAxisOrient = "xup", 
							zeroScaleOrient = True, 
							children = True)
	cmds.xform(shoulderJnt, rotation = shoulderAngle)
	cmds.makeIdentity(shoulderJnt, apply = True, 
								   rotate = True,
								   translate = True,
								   scale = True,
								   preserveNormals = True,
								   normal = False)
	return [shoulderJnt, elbowJoint, wristJoint]

# input a joint name, create a box at joint position and return its name
def createBoxMeshAtJoint(jnt):
	boxMesh = cmds.polyCube(name = "box_" + jnt)[0]
	cmds.select([])
	trans = cmds.xform(jnt, query = True, worldSpace = True, matrix = True)
	cmds.xform(boxMesh, worldSpace = True, matrix = trans)
	cmds.setAttr(boxMesh + ".overrideEnabled", 1)
	cmds.setAttr(boxMesh + ".overrideShading", 0)
	cmds.setAttr(boxMesh + ".overrideColor", 13)
	return boxMesh


# input the joint list, create mesh boxes at each joint
def createBoxMeshList(jntList):
	boxMeshList = []
	for jnt in jntList:
		boxMeshList += [createBoxMeshAtJoint(jnt)]
	return boxMeshList


# input the boxmesh list, create box type for each box
def createBoxList(meshList):
	boxList = []
	for mesh in meshList:
		boxList += [getBoxFromMesh(mesh)]
	return boxList


# The function to skin the mesh to joints
def performSkinning(fakeInput, rootJnt, boxList, jntList, meshList, vertList, skinnedMeshList):
	skinnedMeshList += cmds.ls(selection = True, flatten = True)
	infVertList = []
	skinClusterDic = dict([])

	# bind meshes to the root joint
	for mesh in skinnedMeshList:
		skinCluster = cmds.skinCluster(rootJnt, mesh, toSelectedBones = True)[0]
		skinClusterDic[mesh] = skinCluster

	# get verts into the list
	getVertsFromMesh(skinnedMeshList, vertList)


	# add each joint to influence 
	for index in xrange(len(boxList)):
		box = boxList[index]
		box.updateMath()

		jnt = jntList[index]

		# for each skincluster, add them one by one
		if jnt != rootJnt:
			for mesh in skinClusterDic:
				cmds.skinCluster(skinClusterDic[mesh], edit = True, 
											  		   addInfluence = jnt, 
											  		   weight = 0)

	# calculate weight for each vertex
	for vert in vertList:
		mesh = polyToTrans(vert)
		infJntList = []
		vertPosition = cmds.xform(vert, query = True, translation = True, worldSpace = True)
		for index in xrange(len(boxList)):
			box = boxList[index]
			if box.insideBox(vertPosition):
				infJntList += [jntList[index]]

		# if the vert is assigned to some joint
		if infJntList != []:
			weight = 1.0/len(infJntList)

			# zip joint with skin weight
			jntWeightList = []
			for jnt in infJntList:
				jntWeightList += [(jnt, weight)]

			# set skin weight for the vertex
			cmds.skinPercent(skinClusterDic[mesh], vert, transformValue = jntWeightList)


# input locator name list, create joint chain and one box at each joint
# in addition, add buttons on UI for boxes
def createJointChainAndBox(fakeInput, locList, colLayout):
	vertList = []
	locatorNodeList = locList
	cmds.select([])
	locatorPosList = []
	skinnedMeshList = []
	for loc in locatorNodeList:
		locatorPosList += [cmds.xform(loc, query = True, translation = True, worldSpace = True)]
	jntList = createJointChain(locatorPosList[0], locatorPosList[1], locatorPosList[2])
	meshList = createBoxMeshList(jntList)
	boxList = createBoxList(meshList)
	# UI part
	for meshName in meshList:
		cmds.rowLayout( numberOfColumns = 2, 
						columnAttach = [(1, 'both', 20), (2, "both", 40)], 
						columnWidth=[(1, 200), (2, 250)],
						height = 50,
						parent = colLayout)
		cmds.text(label = meshName)
		cmds.button(label = "select", command = partial(chooseMesh, meshName = meshName))
		cmds.setParent("..")
	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=(1, 'both', 135), 
					columnWidth=(1, 250),
					height = 50 )
	cmds.button( label='Bind Skin', 
				 command = partial(performSkinning, rootJnt = jntList[0],
				 									meshList = meshList,
				 									jntList = jntList,
				 								    boxList = boxList, 
				 								    vertList = vertList,
				 								    skinnedMeshList = skinnedMeshList), 
				 								 	width = 250)
	cmds.setParent("..")




# function to create locators
# in addition, create the row for each locator in UI
def createLocators(fakeInput, num, locList, colLayout):

	# for the number of creators
	for i in xrange(num):
		# create locator
		locName = cmds.spaceLocator(name = "armLocator_temp_" + str(i+1))
		locList += [locName]
		cmds.select([])
		# do UI part
		cmds.rowLayout( numberOfColumns = 2, 
						columnAttach = [(1, 'both', 20), (2, "both", 40)], 
						columnWidth=[(1, 200), (2, 250)],
						height = 50 )
		cmds.text(label = "armLocator_temp_" + str(i+1))
		cmds.button(label = "select", command = partial(chooseMesh, meshName = locName))
		cmds.setParent("..")
	
	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=(1, 'both', 135), 
					columnWidth=(1, 250),
					height = 50 )
	cmds.button( label='Confirm Locators', 
				 command = partial(createJointChainAndBox, locList = locList, 
				 										   colLayout = colLayout), 
				 	   width = 250)
	cmds.setParent("..")

# The real UI function
def win(fakeInput = True):
	win_Name = "PandaMenu Auto Rigging Tool - Arm"
	versionNumber = 0.1

	#if old ui not closed, close it
	if cmds.window(win_Name, exists = True):
		cmds.deleteUI(win_Name)
	window = cmds.window(win_Name, sizeable = True,
							titleBar = True, resizeToFitChildren = True,
							menuBar = True,
							title = win_Name + " ver " + str(versionNumber))

	#global list that contains cross-window selection names
	vertList = []
	polyList = []
	locList = []
	existedTypeList = []



	#col layout
	colLayout = cmds.columnLayout()

	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=(1, 'both', 135), 
					columnWidth=(1, 250),
					height = 50 )
	cmds.button( label='Create Locators', 
				 command = partial(createLocators, num = 3, 
				 								   locList = locList, 
				 								   colLayout = colLayout), 
				 width = 250)
	cmds.setParent("..")
	cmds.showWindow( window )