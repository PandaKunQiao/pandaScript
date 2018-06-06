import maya.cmds as cmds
from functools import partial

def getAllConstraintFromScene(fake_input = True):
    meshTransList = []
    
    for eachCons in cmds.ls(type = "parentConstraint"):
        #print eachTrans
        cmds.setAttr(eachCons+".interpType", 2)
    for eachCons in cmds.ls(type = "orientConstraint"):
        #print eachTrans
        cmds.setAttr(eachCons+".interpType", 2)
        


def win(fake_input = True):
    winName = "Change Constraint Interp type"
    versionNumber = 0.1
    
    if cmds.window(winName, exists = True):
        cmds.deleteUI(winName)

    cmds.window(winName, sizeable = True,
                titleBar = True, resizeToFitChildren = False,
                menuBar = True, widthHeight = (600, 500),
                title = winName)
    cmds.columnLayout(columnWidth = 600, rowSpacing = 20)
    cmds.rowLayout(numberOfColumns=1, columnAttach = [1, "both", 0])
    cmds.button(label = "shortest", command = partial(getChosenTransFromScene))
    cmds.setParent("..")
    cmds.showWindow()
