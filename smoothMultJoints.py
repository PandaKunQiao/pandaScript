import maya.cmds as cmds
from functools import partial
import maya.mel as mel
import math
import string
import numpy as np

# def getWeightMap():
# 	for joint in cmds.ls(select = True):

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
	cmds.select(vertex)

	# the vertex must be selected, this function returns a string ["num1 num2 num3 num4"]
	indexString = cmds.polyInfo(vertexToFace = True)[0]
	indexList = infoToIndex(indexString)
	faceList = indexToPoly(transName, "f", indexList)
	return faceList

# input: face
# output: [vert, vert, vert...]
def faceToAdjacentVertex(face):
	transName = polyToTrans(face)
	cmds.select(face)
	indexString = cmds.polyInfo(faceToVertex = True)[0]
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
	return vertList

# input: skincluter, vertex
# output: [[joint, jointWeight], [joint, jointWeight], ....]
def getInfluencingJoints(skinCluster, vertex):
	jointList = cmds.skinPercent(skinCluster, vertex, query = True, ignoreBelow = 0.001, transform = None)
	resultList = []
	for i in xrange(len(jointList)):
		resultList += [[jointList[i], cmds.skinPercent(skinCluster, vertex, query = True, transform = jointList[i])]]
	return resultList

# input: vertex list that need to be smoothed, joint list that need to be smoothed, the applied skin cluster
# output: [[vert, sum of vertweights over the joint list, sum of new vert weights over the joint list, [jnt, vertweight(unnormalized)]], ...]
def appliedKernel(vertList, jntList, skinCluster):
	result = []
	for vert in vertList:
		eachVertList = []
		eachVertWeight = 0.0
		eachVertNewWeight = 0
		for jnt in jntList:
			eachVertWeight += (cmds.skinPercent(skinCluster, vert, query = True, transform = jnt))
			adjVtxList = list(set(vertexToAdjacentVertices(vert)))
			weightSum = 0
			for i in xrange(len(adjVtxList)):
				weightSum += cmds.skinPercent(skinCluster, adjVtxList[i], query = True, transform = jnt)
			weight = weightSum/len(adjVtxList)
			eachVertNewWeight += weight
			eachVertList += [[jnt, weight]]

		result += [[vert, eachVertWeight, eachVertNewWeight, eachVertList]]
	return result

# input: skinCluster, output of applied kernel
# output: [[(jnt, appliedweight), (jnt, appliedweight), (jnt, appliedweight), ...], ...]
# side effects: smooth the skin for selected vertices over the selected joints
def normalizeWeight(skinCluster, infoList):
	result = []
	for i in xrange(len(infoList)):
		vert = infoList[i][0]
		eachVertWeight = infoList[i][1]
		eachVertNewWeight = infoList[i][2]
		eachVertList = infoList[i][3]
		eachVertNewInfo = []
		for info in eachVertList:
			jnt = info[0]
			weight = info[1]
			eachVertNewInfo += [(jnt, (weight / eachVertNewWeight *eachVertWeight))]
		cmds.skinPercent(skinCluster, vert, transformValue = eachVertNewInfo)
		result += [eachVertNewInfo]
	return result



# user interface


# get vertices
def getVerts(fakeInput, vertList):
	vertList += cmds.ls(selection = True, flatten = True)
	print vertList
	return None

# put joints into the list
def getJoints(fakeInput, jntList):
	jntList += cmds.ls(selection = True)
	print jntList
	return None

def smoothButton(fakeInput, jntList, vertList, txtField1, txtField2):
	numOfIterations = int(cmds.textField(txtField1, text = True, query = True))
	skinCluster = cmds.textField(txtField2, text = True, query = True)
	for i in xrange(numOfIterations):
		infoList = appliedKernel(vertList, jntList, skinCluster)
		print normalizeWeight(skinCluster, infoList)

def win(fakeinput = True):
	win_Name = "PandaMenu Smooth Skin Weights"
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
	jntList = []



	#col layout
	cmds.columnLayout(columnAttach=('left', 5))

	#first row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'Number of Iterations' )
	txtField1 = 	cmds.textField(text = "1")
	cmds.setParent("..")


	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.text( label = 'SkinCluster Name' )
	txtField2 = cmds.textField(text = "")
	cmds.setParent("..")

	#second row layout
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'both', 0), (2, "both", 10)], 
					columnWidth=[(1, 150), (2, 250)],
					height = 25 )
	cmds.button( label = 'Confirm Joints', command = partial(getJoints, jntList = jntList))
	cmds.button(label = "Confirm Vertices", command = partial(getVerts, vertList = vertList))
	cmds.setParent("..")


	#the button
	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=[(1, 'both', 0)],
					columnWidth = (1, 400), 
					height = 50 )
	cmds.button(label = "Smooth", command = partial(smoothButton, jntList = jntList, vertList = vertList, txtField1 = txtField1, txtField2 = txtField2))
	cmds.showWindow( window )