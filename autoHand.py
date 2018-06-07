import maya.cmds as cmds
from functools import partial
import maya.mel as mel
import math
import string
import copy
import numpy as np
from polyLib import *

# for hand controls

# finger ctrl chians
THUMBCTRLCHAIN = 	["ctrl_l_thumb_A", "ctrl_l_thumb_B", "ctrl_l_thumb_C"]
INDEXCTRLCHAIN = 	["ctrl_l_index_A", "ctrl_l_index_B", "ctrl_l_index_C"]
MIDDLECTRLCHAIN = 	["ctrl_l_middle_A", "ctrl_l_middle_B", "ctrl_l_middle_C"]
RINGCTRLCHAIN = 	["ctrl_l_ring_A", "ctrl_l_ring_B", "ctrl_l_ring_C"]
LITTLECTRLCHAIN = 	["ctrl_l_little_A", "ctrl_l_little_B", "ctrl_l_little_C"]
FINGERCTRLCHAIN = 	["ctrl_l_thumb_A", "ctrl_l_thumb_B", "ctrl_l_thumb_C", 
					"ctrl_l_index_A", "ctrl_l_index_B", "ctrl_l_index_C", 
					"ctrl_l_middle_A", "ctrl_l_middle_B", "ctrl_l_middle_C", 
					"ctrl_l_ring_A", "ctrl_l_ring_B", "ctrl_l_ring_C", 
					"ctrl_l_little_A", "ctrl_l_little_B", "ctrl_l_little_C"]
PALMCTRL = "ctrl_l_palm"

# assisting cube names
HANDCUBE = "cube_l_hand"
THUMBCUBE = "cube_l_thumb"
INDEXCUBE = "cube_l_index"
MIDDLECUBE = "cube_l_middle"
RINGCUBE = "cube_l_ring"
LITTLECUBE = "cube_l_little"

THUMBPOSCHAIN = [[0.130560543603, 0.0,2.19703176249], [1.03882659081, 0.0,2.19703176249], [1.95546050229, 0.0,2.19703176249]]
INDEXPOSCHAIN = [[2.13147675473, 0.0,1.1332830162], [3.1193908792, 0.0,1.1332830162], [4.11988348897, 0.0,1.1332830162]]
MIDDLEPOSCHAIN = [[2.46978781997, 0.0,0.0725509862787], [3.45770194445, 0.0,0.0725509862787], [4.45819455422, 0.0,0.0725509862787]]
RINGPOSCHAIN = [[2.25476425876, 0.0,-1.06715983925], [3.24267838324, 0.0,-1.06715983925], [4.24317099301, 0.0,-1.06715983925]]
LITTLEPOSCHAIN = [[1.94568953348, 0.0,-2.10400081347], [2.93360365796, 0.0,-2.10400081347], [3.93409626773, 0.0,-2.10400081347]]


FINGERPOSCHAIN = [
[0.130560543603, 0.0,2.19703176249], [1.03882659081, 0.0,2.19703176249], [1.95546050229, 0.0,2.19703176249],
[2.13147675473, 0.0,1.1332830162], [3.1193908792, 0.0,1.1332830162], [4.11988348897, 0.0,1.1332830162],
[2.46978781997, 0.0,0.0725509862787], [3.45770194445, 0.0,0.0725509862787], [4.45819455422, 0.0,0.0725509862787],
[2.25476425876, 0.0,-1.06715983925], [3.24267838324, 0.0,-1.06715983925], [4.24317099301, 0.0,-1.06715983925],
[1.94568953348, 0.0,-2.10400081347], [2.93360365796, 0.0,-2.10400081347], [3.93409626773, 0.0,-2.10400081347]
]
PALMPOS = [0.99859768353, 0.0,0.0]

# Finger bounding box chain 
THUMBTRANSFORM = [[1.039, 0, 2.197], [0, 0, 0], [2.775, 1, 1]]
INDEXTRANSFORM = [[3.119, 0, 1.133], [0, 0, 0], [3.015, 1, 1]]
MIDDLETRANSFORM = [[3.458, 0, 0.073], [0, 0, 0], [3.015, 0, 0]]
RINGTRANSFORM = [[3.243, 0, -1.067], [0, 0, 0], [3.015, 1, 1]]
LITTLETRANSFORM = [[2.934, 0, -2.014], [0, 0, 0], [3.015, 1, 1]]


JOINTORIENTLIST = ["arm", "general"]



# generic functions
# get part after prefix
def getMainName(name, prefix):
	mainName = name[len(prefix):]
	print "main name is" + mainName
	return mainName

# add prefix to name
def addPrefix(name, prefix):
	newName = prefix + name
	print "new name is " + newName
	return newName

# add suffix to name
def addSuffix(name, suffix):
	newName = name + suffix
	print "new name is" + newName
	return newName

#helper to select the input node
def selectNode(nodeName, *args):
	cmds.select(nodeName, replace = True)

#helper to close the window
def closeReverseWindow(*args):
	cmds.deleteUI("New_Reverse_Node")


def getWeightAttrName(constraintName, jointName, suffix):
	return constraintName + "." + jointName + suffix

# INPUT: tansform node 1's name, transform node 2's name
# OUTPUT: a float which is the world distance between obj1 and obj2
def calcDistance(obj1, obj2):
	pos1 = cmds.xform(obj1, query = True, translation = True, worldSpace = True)
	pos2 = cmds.xform(obj2, query = True, translation = True, worldSpace = True)
	deltX = pos1[0] - pos2[0]
	deltY = pos1[1] - pos2[1]
	deltZ = pos1[2] - pos2[2]
	dist = (deltX ** 2.0 + deltY ** 2.0 + deltZ ** 2.0) ** 0.5
	return dist
# input: cube name
# output: created cube name
# sideeff:create a cube at (0, 0, 0)
def createCube(cubeName):
	cmds.select([])
	cube = cmds.curve(degree = 1, 
		p = [
		(-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), 
		(-0.5, 0.5, 0.5,), (-0.5, -0.5, 0.5,), (-0.5, -0.5, -0.5), 
		(0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5), 
		(0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), 
		(0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5)
		], 
		knot = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
		name = cubeName)
	cmds.select([])
	return cube

# input: transform's name, translate value, rotate value, scale value
# output: None
# side: transform the transform node at accordingly positions
def setTransAttr(trans, translate = [0, 0, 0], rotate = [0, 0, 0], 
						scale = [1, 1, 1]):
	cmds.setAttr(trans + ".translateX", translate[0])
	cmds.setAttr(trans + ".translateY", translate[1])
	cmds.setAttr(trans + ".translateZ", translate[2])

	cmds.setAttr(trans + ".rotateX", rotate[0])
	cmds.setAttr(trans + ".rotateY", rotate[1])
	cmds.setAttr(trans + ".rotateZ", rotate[2])

	cmds.setAttr(trans + ".scaleX", scale[0])
	cmds.setAttr(trans + ".scaleY", scale[1])
	cmds.setAttr(trans + ".scaleZ", scale[2])

	print "put" + trans + "successfully"


# input: name of root joint
# output: none
# side: orient joints
def orientJntChain(rootJnt, orient = "general"):
	if orient == "arm":
		cmds.joint(rootJnt, edit = True, orientJoint = "xyz", 
							secondaryAxisOrient = "zup", 
							zeroScaleOrient = True, 
							children = True)
	else:
		cmds.joint(rootJnt, edit = True, orientJoint = "xzy", 
							secondaryAxisOrient = "xup", 
							zeroScaleOrient = True, 
							children = True)
	print ("orient joint as" + orient)
	return None



# input: locator list, orient of joints, prefix, suffix
# output: a joint chain list
# side: generic function to create a single joint chain according to the
# orientation
def buildSingleJntChain(locLs, cubeName, orient, prefix, suffix):
	jntLs = []

	# get first joint's location and build it
	jntName = addSuffix(addPrefix(getMainName(locLs[0], "loc_"), prefix),suffix)
	# get position of locator
	transPos = cmds.xform(locLs[0],query = True,translation = True,worldSpace = True)
	# creat the joint
	cmds.select(clear = True)
	crtJnt = cmds.joint(name = jntName)
	cmds.xform(jntName, translation = transPos)

	# for the rest of fingers
	preJnt = crtJnt
	jntLs += [crtJnt]
	for index in xrange(1, len(locLs)):
		# prepare names for each iteration
		preLoc = locLs[index-1]
		loc = locLs[index]
		jntName = addSuffix(addPrefix(getMainName(loc, "loc_"), prefix),suffix)

		# get position of locator
		transPos = calcDistance(loc, preLoc)

		# creat the joint
		crtJnt = cmds.joint(name = jntName)
		cmds.xform(jntName, translation = (transPos, 0, 0))
		preJnt = crtJnt
		jntLs += [crtJnt]

	# define the root joint
	print jntLs
	rootJnt = jntLs[0]


	# orient the joint chain
	cmds.joint(rootJnt, edit = True, orientJoint = "xyz", 
							secondaryAxisOrient = "zup", 
							zeroScaleOrient = True, 
							children = True)

	# rotate the joint to cube's rotation
	cmds.delete(cmds.orientConstraint(cubeName, rootJnt))
	cmds.makeIdentity(cube, apply = True, rotate = True, translate = True,
							scale = True, preserveNormals = True,
							normal = False)
	return jntLs

def createSingleFingerLocs(ctrlLs, posLs, cubeName, cubeTransform):
	locLs = []

	# create finger locators
	for i in xrange(len(ctrlLs)):
		ctrl = ctrlLs[i]
		pos = posLs[i]
		print "ctrl name: " + ctrl
		print "position: " + str(pos)

		locName = addPrefix(getMainName(ctrl, "ctrl_"), "loc_")
		loc = cmds.spaceLocator(name = locName)[0]
		setTransAttr(loc, translate = pos)
		locLs += [loc]

	# create the cube that contains the locators
	cube = createCube(cubeName)
	setTransAttr(cube, cubeTransform[0], cubeTransform[1], cubeTransform[2])
	cmds.makeIdentity(cube, apply = True, rotate = True, translate = True,
							scale = True, preserveNormals = True,
							normal = False)
	cmds.parent(locLs, cube)
	return (cube, locLs)


# input: the control name list of the chain for the finger
# output: a list of locators for the finger
def createFingerLocs(ctrlLs, posLs, palmCtrl, palmPos):

	# make a cube, transform to proper shape and zero out
	cube = createCube(HANDCUBE)
	setTransAttr(cube, translate = [1.775, 0, 0], scale = [8.504, 2.877, 6.367])
	cmds.makeIdentity(cube, apply = True, rotate = True, translate = True,
							scale = True, preserveNormals = True,
							normal = False)


	# create rotation indicators for each finger
	(thumbCube, thumbLocLs) = createSingleFingerLocs(THUMBCTRLCHAIN, 
								THUMBPOSCHAIN, THUMBCUBE, THUMBTRANSFORM)
	(indexCube, indexLocLs) = createSingleFingerLocs(INDEXCTRLCHAIN,
								INDEXPOSCHAIN, INDEXCUBE, INDEXTRANSFORM)
	(middleCube, middleLocLs) = createSingleFingerLocs(MIDDLECTRLCHAIN,
								MIDDLEPOSCHAIN, MIDDLECUBE, MIDDLETRANSFORM)
	(ringCube, ringLocLs) = createSingleFingerLocs(RINGCTRLCHAIN,
								RINGPOSCHAIN, RINGCUBE, RINGTRANSFORM)
	(littleCube, littleLocLs) = createSingleFingerLocs(LITTLECTRLCHAIN,
								LITTLEPOSCHAIN, LITTLECUBE, LITTLETRANSFORM)
	
	# parent locators under the big cube
	cmds.parent([thumbCube, indexCube, middleCube, ringCube, littleCube], cube)

	# create palm locator
	cmds.spaceLocator(name = palmCtrl)
	cmds.parent(palmCtrl, cube)
	return (thumbLocLs + indexLocLs + middleLocLs + ringLocLs + littleLocLs,
		[thumbCube, indexCube, middleCube, ringCube, littleCube])




# input: locList has locators from A to Z 
# output: jntList has joints from A to Z
# side: create a whole chain of finger joints
def buildSingleFingerChain(locLs, cubeLs):
	# call the generic function to build a chain of joint
	return buildSingleJntChain(locLs, cubeName, "finger", "bn_", "_jnt")





# input: loclist has finger locators
# output: jointlist at corresponding positions
# side: create all finger joints
def buildMultFingerJoints(locLs, cubeLs):
	jntLs = []
	fingerRootLs = []
	for i in xrange(5):
		crtFingerJntLs = buildSingleFingerChain(locLs[i*3:(i*3+3)], cubeLs[i])
		jntLs += crtFingerJntLs
		fingerRootLs += [crtFingerJntLs[0]]
	print "build all finger joints successfully"
	print locLs
	palmJnt = buildSingleJntChain([PALMCTRL], HANDCUBE, "palm", "bn_", "_jnt")
	cmds.parent(fingerRootLs, palmJnt)
	jntLs += [palmJnt]
	return jntLs




locs = createFingerLocs(FINGERCTRLCHAIN, FINGERPOSCHAIN, PALMCTRL, PALMPOS)
# buildMultFingerJoints(locs)
