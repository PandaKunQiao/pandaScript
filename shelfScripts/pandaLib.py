import maya.cmds as cmds
from functools import partial
import maya.mel as mel
import math
import string
import copy
import numpy as np
from polyLib import *

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

#helper to select the input node
def selectNode(nodeName, *args):
	cmds.select(nodeName, replace = True)

#helper to close the window
def closeReverseWindow(*args):
	cmds.deleteUI("New_Reverse_Node")

def getWeightAttrName(constraintName, jointName, suffix):
	return constraintName + "." + jointName + suffix

def setTransAttr(trans, translate = [0, 0, 0], rotate = [0, 0, 0], scale = [1, 1, 1]):
	cmds.setAttr(trans + ".translateX", translate[0])
	cmds.setAttr(trans + ".translateY", translate[1])
	cmds.setAttr(trans + ".translateZ", translate[2])

	cmds.setAttr(trans + ".rotateX", rotate[0])
	cmds.setAttr(trans + ".rotateY", rotate[1])
	cmds.setAttr(trans + ".rotateZ", rotate[2])

	cmds.setAttr(trans + ".scaleX", scale[0])
	cmds.setAttr(trans + ".scaleY", scale[1])
	cmds.setAttr(trans + ".scaleZ", scale[2])


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

# input all the ctrls that want enforce parent constraint on
def addParentConstraint(parentLs, childLs):
	if parentLs != childLs:
		print "number of parents is not equal to number of children"
		return None
	for i in xrange(len(parentLs)):
		cmds.addParentConstraint(parentLs[i], childLs[i], maintainOffset = True)