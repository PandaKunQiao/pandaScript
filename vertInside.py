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
		else:
			return "D"

	def printVal(self):
		print self.a
		print "A: " + str(self.a)
		print "B: " + str(self.b)
		print "C: " + str(self.c)
		print "S: " + str(self.s)


# the box is initiated by 3 pairs of planes, which are the faces of the boxes that oppsite with each other
class Box:
	def __init__(self, planeSet1, planeSet2, planeSet3, faceList, level):
		self.planeU = planeSet1[0]
		self.planeD = planeSet1[1]

		self.planeL = planeSet2[0]
		self.planeR = planeSet2[1]

		self.planeF = planeSet3[0]
		self.planeB = planeSet3[1]

		self.faceList = faceList
		self.level = level

	
	def checkFace(self, face):
		return (face in self.faceList)


	def insideBox(self, vertTest):
		if (self.planeU.upOrDown(vertTest) != self.planeD.upOrDown(vertTest) and 
			self.planeL.leftOrRight(vertTest) != self.planeR.leftOrRight(vertTest) and 
			self.planeF.frontOrBack(vertTest) != self.planeB.frontOrBack(vertTest)):
			return True
		else:
			return False

# polygon object has 2 features, one is a dictionary, the other is the number of levels.
# 
# Each polygon is eather a plane or another polygon
class Poly:
	def __init__(self, box):
		self.boxDict = dict([])
		for i in xrange(len(faceList)):
			self.boxDict[faceList[i]] = box
		self.numLevel = 1

	# first iterate through all levels, and check each box's inside objects. 
	# If they are in the previous ones, delete them, if not, add them
	def insidePoly(self, vertList):
		chosenSet = set([])
		for i in xrange(self.numLevel):
			for j in xrange(len(self.levelList[i])):
				box =levelList[i][j]
				vertInBox = set(box.insideBox(vertList))
				if chosenSet & vertInBox == vertInBox:
					chosenSet -= vertInBox
				else:
					chosenSet += vertInBox
		return list(chosenSet)

	# given the extended face and the new face list, update the poly with
	# new box
	def updatePoly(self, origFace, newFaceList, box):

		# update the old box attributes
		oldBox = self.boxDict[origFace]
		oldBox.faceList.remove(origFace)

		# update the new poly attributes
		self.dict[origFace] = box
		for i in xrange(len(newFaceList)):
			self.dict[newFaceList[i]] = box
		if box.level == self.numLevel:
			self.numLevel += 1
		return None

# given the mesh meshvertices list and mesh face list, create a new polygon from one cube
# vertlist are integers, facelist are face indices
def createPoly(mesh, meshVertList, meshFaceList):
	box = createBox(mesh, meshVertList, meshFaceList, 0)
	poly = Poly(box)
	return poly


# given the polygon and mesh's name, the name to add division, return the new poly
def addPolyFace(poly, mesh, face):
	faceName = mesh+".[" + str(face) + "]"
	cmds.polyExtrudeFacet(faceName, localScale=(0.5, 0.5, 0.5))
	newFaceList = faceToAdjacentFaces(faceName)
	poly.updatePoly()
	
		

# the function to create a box object from maya mesh
def createBox(mesh, meshVertList, meshFaceList, level):

	# sort positions of vertices in x, y and z directions
	xList = copy.deepcopy(meshVertList)
	yList = copy.deepcopy(meshVertList)
	zList = copy.deepcopy(meshVertList)
	positionList = []
	for i in meshVertList:
		meshVert = mesh + ".vtx[" + str(i) + "]"
		positionList += [cmds.xform(meshVert, query = True, translation = True)]
	xList.sort(key=lambda x: positionList[x][0])
	yList.sort(key=lambda x: positionList[x][1])
	zList.sort(key=lambda x: positionList[x][2])

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
					vertLTB = vertName
				else:
					vertLTF = vertName
			else:
				if (i in zList[0:4]):
					vertLBB = vertName
				else:
					vertLBF = vertName
		else:
			if (i in yList[0:4]):
				if (i in zList[0:4]):
					vertRTB = vertName
				else:
					vertRTF = vertName
			else:
				if (i in zList[0:4]):
					vertRBB = vertName
				else:
					vertRBF = vertName

	# create box
	posList = [-1]
	posList += [cmds.xform(vertLTB, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertLTF, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertRTF, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertRTB, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertRBB, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertRBF, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertLBF, query = True, translation = True, worldSpace = True)]
	posList += [cmds.xform(vertLBB, query = True, translation = True, worldSpace = True)]


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
		faceList += [mesh + ".[" + str(i) + "]"]

	return Box([planeA1, planeA2], [planeB1, planeB2], [planeC1, planeC2], faceList, level)


# the function to create a box from maya mesh
def getBoxFromView():
	mesh = cmds.ls(selection = True)[0]
	meshFaceList = range(8)
	meshVertList = range(8)
	return createBox(mesh, meshVertList, meshFaceLsit)








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

def testPlaneAll(side):
	selectionList = []
	plane = getPlaneFromView()
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

def testUDPlaneOne(side):
	selectionList = []
	plane = getPlaneFromView()
	plane.printVal()
	cubeName = "pCube289"
	result = plane.upOrDown(cmds.xform(cubeName, translation = True, worldSpace = True, query = True))
	print result
	if  result == side:
		cmds.select(selectionList)



def testBoxAll():
	selectionList = []
	box = getBoxFromView()
	for i in xrange(288):
		cubeName = "pCube" + str(i+1)
		if box.insideBox(cmds.xform(cubeName, translation = True, worldSpace = True, query = True)):
			selectionList += [cubeName]
	cmds.select(selectionList)

def testBoxOne():
	selectionList = []
	box = getBoxFromView()
	cubeName = "pCube289"
	if box.insideBox(cmds.xform(cubeName, translation = True, worldSpace = True, query = True)):
		selectionList += [cubeName]


testBoxAll()