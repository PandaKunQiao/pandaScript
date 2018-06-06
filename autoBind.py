import maya.cmds as cmds
from functools import partial
import maya.mel as mel
import math
import string
import copy
import numpy as np

# input: root joint, mesh container, skincluster dictionary
# side effect: bind all chosen mesh to the root joint
# return none
def bindToRootJoint(fakeInput,
					rootJoint, 
					globalMeshList,
					globalSkinClusterDict):
	globalMeshList += cmds.ls(selection = True, flatten = True)
	for mesh in globalMeshList:
		skinCluster = cmds.skinCluster(rootJoint, mesh)[0]
		globalSkinClusterDict[mesh] = skinCluster

# input: root joint list 
# side effect:create root joint
# output: none
def createRootJoint(fakeInput,
					globalMeshList, 
					globalRootJntList, 
					globalSkinClusterDict
					):
	rootJoint = cmds.joint(name = "temp_root")
	globalRootJntList += [rootJoint]
	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=(1, 'both', 135), 
					columnWidth=(1, 250),
					height = 50 )
	cmds.text(label = "Choose all meshes to be binded")
	cmds.setParent("..")

	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=(1, 'both', 135), 
					columnWidth=(1, 250),
					height = 50 )
	cmds.button( label='Bind to Root Joint', 
				 command = partial(bindToRootJoint, 
				 				   rootJoint = rootJoint,
				 				   globalMeshList = globalMeshList,
				 				   globalSkinClusterDict = globalSkinClusterDict), 
				 width = 250)
	cmds.setParent("..")

# main window
# input the container for binded mesh, root and skincluster
def bindWin(fakeInput, globalMeshList, globalRootJntList, globalSkinClusterDict):
	win_Name = "Bind Skin"
	versionNumber = 0.1

	#if old ui not closed, close it
	if cmds.window(win_Name, exists = True):
		cmds.deleteUI(win_Name)
	window = cmds.window(win_Name, sizeable = True,
								   titleBar = True, resizeToFitChildren = True,
								   menuBar = True,
								   title = win_Name + " ver " + str(versionNumber))

	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=(1, 'both', 135), 
					columnWidth=(1, 250),
					height = 50 )
	cmds.button( label='Create Root Joint', 
				 command = 
				 	partial(createRootJoint, 
				 			globalMeshList = globalMeshList,
				 			globalRootJntList = globalRootJntList,
				 			globalSkinClusterDict = globalSkinClusterDict), 
				 width = 250)
	cmds.setParent("..")
	cmds.showWindow(window)