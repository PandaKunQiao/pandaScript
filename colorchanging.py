import maya.cmds as cmds
from functools import partial

def pressEnter(input_command, input_shape, *args):
    crt_color = cmds.textField(input_command, q = True, text = True)
    cmds.setAttr(input_shape+".overrideEnabled", 1)
    if crt_color == "bred":
        cmds.setAttr(input_shape+".overrideColor", 13)
    elif crt_color == "blue":
        cmds.setAttr(input_shape+".overrideColor", 15)
    elif crt_color == "yellow":
        cmds.setAttr(input_shape+".overrideColor", 17)
    elif crt_color == "green":
        cmds.setAttr(input_shape+".overrideColor", 14)
    elif crt_color == "gray":
        cmds.setAttr(input_shape+".overrideColor", 1)
    elif crt_color == "pink":
        cmds.setAttr(input_shape+".overrideColor", 9)
    elif crt_color == "bblue":
        cmds.setAttr(input_shape+".overrideColor", 6)
    elif crt_color == "red":
        cmds.setAttr(input_shape+".overrideColor", 12)
    elif crt_color == "lblue":
        cmds.setAttr(input_shape+".overrideColor", 18)

    else:
        cmds.error("color not in library")
def enterAllColors(input_command, input_tuple_list, *args):
    for input_tuple in input_tuple_list:
        pressEnter(input_command, input_tuple[1])
def swipeColor(crt_Shape, *args):
    cmds.setAttr(crt_Shape+".overrideEnabled", 1)
    crt_colorIndex = int(cmds.getAttr(crt_Shape+".overrideColor"))
    if crt_colorIndex >= 30:
        crt_colorIndex = 1
    else:
        crt_colorIndex += 1
    cmds.setAttr(crt_Shape+".overrideColor", crt_colorIndex)
    print crt_colorIndex

def swipeAllColor(tupleList, *args):
    for shape in tupleList:
        swipeColor(shape[1])
    
def all_ctrl_win(fake_input = True):
    winName = "All Controls"
    versionNumber = 0.1
    
    if cmds.window(winName, exists = True):
        cmds.deleteUI(winName)
    
    cmds.window(winName, sizeable = True,
                titleBar = True, resizeToFitChildren = False,
                menuBar = True, widthHeight = (600, 500),
                title = winName)
    
    cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
    cmds.columnLayout(columnAttach=('left', 5), rowSpacing=10, columnWidth=250)
    
    meshTransList = getAllTransFromScene()
    #print meshTransList
    for eachTuple in meshTransList:
        eachTran = eachTuple[0]
        eachShape = eachTuple[1]
        cmds.rowLayout(numberOfColumns=6, columnWidth6=(200, 75, 75, 75, 75, 75), columnAlign=(1, 'center'))
        cmds.text(label = eachTran)
        cmds.button(label = "select", command = partial(selectLabeledTrans, eachTran))
        
        cmds.text(label = "color: ")
        cmds.button(label = "swipe", command = partial(swipeColor, eachShape))
        crt_colorText = cmds.textField(width = 50)
        cmds.textField(crt_colorText, width = 50, enterCommand = partial(pressEnter, crt_colorText, eachShape), alwaysInvokeEnterCommandOnReturn = True, edit = True)

        
        cmds.setParent("..")

    cmds.showWindow()

def selectLabeledTrans(inputName, *args):
    cmds.select(inputName, replace = True)

def testFunc(input = 0, *args):
    print input
    print args
    
def getAllTransFromScene():
    meshTransList = []
    
    for eachTrans in cmds.ls(type = "transform"):
        #print eachTrans
        crt_tree = cmds.listRelatives(eachTrans, children = True, fullPath = True)
        
        if crt_tree != None:
            
            for eachChild in cmds.listRelatives(eachTrans, children = True, fullPath = True):
                
                if cmds.nodeType(eachChild) == "nurbsCurve":
                    
                    if eachTrans not in meshTransList:
                        
                        meshTransList.append((eachTrans, eachChild))
                    
    return meshTransList

def getChosenTransFromScene():
    meshTransList = []
    
    for eachTrans in cmds.ls(type = "transform", selection = True):
        #print eachTrans
        crt_tree = cmds.listRelatives(eachTrans, children = True, fullPath = True)
        
        if crt_tree != None:
            
            for eachChild in cmds.listRelatives(eachTrans, children = True, fullPath = True):
                
                if cmds.nodeType(eachChild) == "nurbsCurve":
                    
                    if eachTrans not in meshTransList:
                        
                        meshTransList.append((eachTrans, eachChild))
                    
    return meshTransList

def chosen_win(fake_input = True):
    winName = "All Controls"
    versionNumber = 0.1
    
    if cmds.window(winName, exists = True):
        cmds.deleteUI(winName)
    
    cmds.window(winName, sizeable = True,
                titleBar = True, resizeToFitChildren = False,
                menuBar = True, widthHeight = (600, 500),
                title = winName)
    
    cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
    cmds.columnLayout(columnAttach=('left', 5), rowSpacing=10, columnWidth=250)
    
    meshTransList = getChosenTransFromScene()
    #print meshTransList
    for eachTuple in meshTransList:
        eachTran = eachTuple[0]
        eachShape = eachTuple[1]
        cmds.rowLayout(numberOfColumns=6, columnWidth6=(200, 75, 75, 75, 75, 75), columnAlign=(1, 'center'))
        cmds.text(label = eachTran)
        cmds.button(label = "select", command = partial(selectLabeledTrans, eachTran))
        
        cmds.text(label = "color: ")
        cmds.button(label = "swipe", command = partial(swipeColor, eachShape))
        crt_colorText = cmds.textField(width = 50)
        cmds.textField(crt_colorText, width = 50, enterCommand = partial(pressEnter, crt_colorText, eachShape), alwaysInvokeEnterCommandOnReturn = True, edit = True)

        
        cmds.setParent("..")
    cmds.rowLayout(numberOfColumns=6, columnWidth6=(200, 75, 75, 75, 75, 75), columnAlign=(1, 'center'))
    cmds.text(label="Change All Colors")
    cmds.text(label="color: ")
    cmds.button(label = "swipe", command = partial(swipeAllColor, meshTransList))
    colorText = cmds.textField(width = 50)
    cmds.textField(colorText, width = 50, enterCommand = partial(enterAllColors, colorText, meshTransList), alwaysInvokeEnterCommandOnReturn = True, edit = True)
    cmds.setParent("..")
    cmds.showWindow()

def win(fake_input = True):
    winName = "Change Controller Color"
    versionNumber = 0.1
    
    if cmds.window(winName, exists = True):
        cmds.deleteUI(winName)

    cmds.window(winName, sizeable = True,
                titleBar = True, resizeToFitChildren = False,
                menuBar = True, widthHeight = (600, 500),
                title = winName)
    cmds.columnLayout(columnWidth = 600, rowSpacing = 20)
    cmds.rowLayout(numberOfColumns=1, columnAttach = [1, "both", 0])
    cmds.button(label = "Show Chosen Controls", command = partial(chosen_win))
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns=1, columnAttach = [1, "both", 0])
    cmds.button(label = "Show All Controls", command = partial(all_ctrl_win))
    cmds.setParent("..")
    cmds.showWindow()
