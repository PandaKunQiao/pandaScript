import maya.cmds as cmds
from functools import partial
import maya.mel as mel
import math
import string
import copy
import numpy as np
import autoBind as bd
import autoArm as arm
import mirrorRig as mir

def legHolder(fakeInput):
	print "leg"

def spineHolder(fakeInput):
	print "spine"

def headHolder(fakeInput):
	print "head"

# The real UI function
def win(fakeInput = True):
	win_Name = "PandaMenu Auto Rigging Tool"
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
	globalMeshList = []
	globalRootJntList = []
	globalSkinClusterDict = dict([])

	globalLeftArmJntList = []
	globalLeftFKArmJntList = []
	globalLeftIKArmJntList = []
	globalLeftArmControlTypeList = ["FK Arm"]
	globalLeftArmCtrlList = [[], [], []]

	globalRightArmJntList = []
	globalRightFKArmJntList = []
	globalRightIKArmJntList = []
	globalRightArmControlTypeList = ["FK Arm"]
	globalRightArmCtrlList = [[], [], []]



	#col layout
	colLayout = cmds.columnLayout()

	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=(1, 'both', 135), 
					columnWidth=(1, 250),
					height = 50 )
	cmds.button( label='Create SkinCluster', 
				 command = partial(bd.bindWin, globalMeshList = globalMeshList, 
				 							   globalRootJntList = globalRootJntList, 
				 							   globalSkinClusterDict = globalSkinClusterDict), 
				 width = 250)
	cmds.setParent("..")

	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=(1, 'both', 135), 
					columnWidth=(1, 520),
					height = 50 )
	cmds.button( label='Create Spine', 
				 command = partial(spineHolder), 
				 width = 250)
	cmds.setParent("..")
	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'left', 135), (2, "right", 135)], 
					columnWidth=[(1, 105), (2, 105)],
					height = 50 )
	cmds.button( label='Create Left Arm', 
				 command = partial(arm.armWin, globalRootJntList = globalRootJntList, 
				 							   globalArmJntList = globalLeftArmJntList,
				 							   globalFKArmJntList = globalLeftFKArmJntList,
				 							   globalIKArmJntList = globalLeftIKArmJntList,
				 							   globalMeshList = globalMeshList,
				 							   globalSkinClusterDict = globalSkinClusterDict,
				 							   globalArmControlTypeList = globalLeftArmControlTypeList,
				 							   globalArmCtrlList = globalLeftArmCtrlList,
				 							   globalDirectionList = ["l"]),
				 width = 125)
	cmds.button( label='Create Right Arm', 
				 command = partial(arm.armWin, globalRootJntList = globalRootJntList, 
				 							   globalArmJntList = globalRightArmJntList,
				 							   globalFKArmJntList = globalRightFKArmJntList,
				 							   globalIKArmJntList = globalRightIKArmJntList,
				 							   globalMeshList = globalMeshList, 
				 							   globalSkinClusterDict = globalSkinClusterDict,
				 							   globalArmControlTypeList = globalRightArmControlTypeList,
				 							   globalArmCtrlList = globalRightArmCtrlList,
				 							   globalDirectionList = ["r"]),
				 width = 125)
	cmds.setParent("..")


	cmds.rowLayout( numberOfColumns=2, 
					columnAttach=[(1, 'left', 135), (2, "right", 135)], 
					columnWidth=[(1, 105), (2, 105)],
					height = 50 )
	cmds.button( label='Mirror Left to Right', 
				 command = partial(mir.mirror, 
				 							   inputJntList = globalLeftArmJntList,
				 							   outputJntList = globalRightArmJntList,
											   inputFKJntList = globalLeftFKArmJntList,
											   outputFKJntList = globalRightFKArmJntList , 
											   inputIKJntList = globalLeftIKArmJntList, 
											   outputIKJntList = globalRightIKArmJntList,
											   inputIKCtrlList = globalLeftArmCtrlList[1],
											   inputFKCtrlList = globalLeftArmCtrlList[0],
											   inputSwitchCtrlList = globalLeftArmCtrlList[2],
											   outputIKCtrlList = globalRightArmCtrlList[1], 
											   outputFKCtrlList = globalRightArmCtrlList[0], 
											   outputSwitchCtrlList = globalRightArmCtrlList[2],
											   inputDirectionList = ["l"], 
											   outputDirectionList = [],
											   ctrlTypeList = globalLeftArmControlTypeList),
				 width = 125)
	cmds.button( label='Mirror Right Arm to Left', 
				 command = partial(mir.mirror, inputJntList = globalRightArmJntList,
				 							   outputJntList = globalLeftArmJntList,
											   inputFKJntList = globalRightFKArmJntList,
											   outputFKJntList = globalLeftFKArmJntList , 
											   inputIKJntList = globalRightIKArmJntList, 
											   outputIKJntList = globalLeftIKArmJntList,
											   inputIKCtrlList = globalRightArmCtrlList[1],
											   inputFKCtrlList = globalLeftArmCtrlList[0],
											   inputSwitchCtrlList = globalRightArmCtrlList[2],
											   outputIKCtrlList = globalLeftArmCtrlList[1], 
											   outputFKCtrlList = globalRightArmCtrlList[0], 
											   outputSwitchCtrlList = globalLeftArmCtrlList[2],
											   inputDirectionList = ["r"], 
											   outputDirectionList = [],
											   ctrlTypeList = globalRightArmControlTypeList),
				 width = 125)
	cmds.setParent("..")


	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=(1, 'both', 135), 
					columnWidth=(1, 250),
					height = 50 )
	cmds.button( label='Create Head', 
				 command = partial(headHolder), 
				 width = 250)
	cmds.setParent("..")
	cmds.rowLayout( numberOfColumns=1, 
					columnAttach=(1, 'both', 135), 
					columnWidth=(1, 250),
					height = 50 )
	cmds.button( label='Create Leg', 
				 command = partial(legHolder), 
				 width = 250)
	cmds.setParent("..")
	cmds.showWindow( window )
win()