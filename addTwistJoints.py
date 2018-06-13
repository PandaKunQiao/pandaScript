import maya.cmds as cmds

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

def addTwistJntsBetween(jnt1, jnt2, name):
	totalDist = cmds.getAttr(jnt2 + ".translateX")
	eachDist = totalDist/4.0
	cmds.select(jnt1, add = False)
	prevJnt = cmds.joint(name = "bn_" + name + "_twist1_jnt")
	for i in xrange(4):
		cmds.select(prevJnt, add = False)
		crtJnt = cmds.joint(name = "bn_" + name + "_twist" + str(i+2) + "_jnt")
		setTransAttr(crtJnt, translate = [eachDist, 0, 0])
		prevJnt = crtJnt

addTwistJntsBetween(cmds.ls(selection = True)[0],cmds.ls(selection = True)[1], "upper")