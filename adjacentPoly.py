# Choose adjacent poly library
# Functions are used to choose poly's adjacent polies
import maya.cmds as cmds
from functools import partial
import maya.mel as mel
import math
import string
import copy
import numpy as np

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