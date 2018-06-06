import maya.cmds as cmds
from functools import partial

def quickOrient(fake_input = True):
    meshTransList = []
    
    for eachCons in cmds.ls(type = "parentConstraint"):
        #print eachTrans
        cmds.setAttr(eachCons+".interpType", 2)
    for eachCons in cmds.ls(type = "orientConstraint"):
        #print eachTrans
        cmds.setAttr(eachCons+".interpType", 2)
        

quickOrient()