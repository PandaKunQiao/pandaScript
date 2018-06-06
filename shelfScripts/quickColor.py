import maya.cmds as cmds

# global colors set by user, this color setting should be done in scripts editor, 
# the follwoings are default values
LCOLOR = "blue"
RCOLOR = "red"
MCOLOR = "yellow"


    
# function that change color accroding to set color and direction of the control
def changeColor(input_shape, direction):
    if direction == "l":
        crt_color = LCOLOR
    elif direction == "r":
        crt_color = RCOLOR
    else:
        crt_color = MCOLOR
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
    return None



# function to get all the shape and transform node in the scene
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


meshTransList = getChosenTransFromScene()
for mesh in meshTransList:
    changeColor(mesh[1], mesh[0][5])