import maya.cmds as cmds
from functools import partial

def quickShowJnt(fake_input = True):
    jntList = []
    
    for eachJnt in cmds.ls(type = "joint"):
        #print eachTrans
        cmds.setAttr(eachJnt+".drawStyle", 0)
        
quickShowJnt()