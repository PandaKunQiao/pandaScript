#cumstom menu by Fred Qiao
import maya.cmds as cmds
from functools import partial
import maya.mel as mel
import math
import string

def getName(fullname):
	start_position = string.rfind(fullname, "|")+1
	return fullname[start_position:]


def storeOptionMenu(item, spaceHolder):
	if spaceHolder == []:
		spaceHolder += [item]
	else:
		spaceHolder[0] = item
	print spaceHolder
	

def getLocPosition(axis):
	if axis == "X":
		return [1, 0, 0]
	elif axis == "Y":
		return [0, 1, 0]
	else:
		return [0, 0, 1]




def createDrivers(fake_input, fbAxis, lrAxis):
	ls_joints = cmds.ls(selection = True)
	cmds.xform(ls_joints)

	for i in xrange(len(ls_joints)):

		# get the position of joint
		joint_position = cmds.xform(ls_joints[0], 
									query = True, 
									world = True, 
								    matrix = True)

		# name of the joint
		joint_name = getName(ls_joints[0])

		# create mid locator, stay locator and move locator
		mid_loc = cmds.spaceLocator("loc_" + joint_name + "_mid", 
									world = True)
		fb_move_loc = cmds.spaceLocator("loc_" + joint_name + "_move_fb", 
									world = True)		
		fb_stay_loc = cmds.spaceLocator("loc_" + joint_name + "_stay_fb", 
									world = True)

		# put move and stay to the right position
		cmds.parent(fb_move_loc, mid_loc)
		cmds.xform(fb_move_loc, translation = getLocPosition(lrAxis))

		cmds.parent(fb_stay_loc, mid_loc)
		cmds.xform(fb_stay_loc, translation = getLocPosition(lrAxis))

		# zero out moving loc
		ref_move = cmds.createNode("transform", name = "ref_loc_" + joint_name + "_move_fb")
		move_position = cmds.xform(fb_move_loc, query = True)
		cmds.


		


# window functions

def win(fake_input = True):
    winName = "Stable Blendshape Driver Creating Tool"
    versionNumber = 0.1

    if cmds.window(winName, exists = True):
        cmds.deleteUI(winName)
    mainWin = cmds.window(winName, sizeable = True,
                         titleBar = True, resizeToFitChildren = True,
                         menuBar = True, widthHeight = (500, 100),
                         title = winName)
    # declare storage arrays:
    fbAxis_var = ["X"]
    lrAxis_var = ["Y"]


    cmds.columnLayout(columnWidth = 300, rowSpacing = 20)

    # menu to choose forward back rotation axis
    cmds.rowLayout(numberOfColumns = 1, columnAttach1 = "both", columnOffset1 = 80)
    cmds.optionMenu(label = "Forward back rotation axis", 
    				changeCommand = partial(storeOptionMenu, spaceHolder = fbAxis_var))
    cmds.menuItem( label='X' )
    cmds.menuItem( label='Y' )
    cmds.menuItem( label='Z' )
    cmds.setParent("..")


    # menu to choose left right rotation axis
    cmds.rowLayout(numberOfColumns = 1, columnAttach1 = "both", columnOffset1 = 80)
    cmds.optionMenu(label = "Left right rotation axis", 
    				changeCommand = partial(storeOptionMenu, spaceHolder = lrAxis_var))
    cmds.menuItem( label='X' )
    cmds.menuItem( label='Y' )
    cmds.menuItem( label='Z' )
    cmds.setParent("..")

    # create drivers
    cmds.rowLayout(numberOfColumns = 1, columnAttach1 = "both", columnOffset1 = 150)
    cmds.button(label = "Create Drivers", command = partial())
    cmds.showWindow(mainWin)
win()