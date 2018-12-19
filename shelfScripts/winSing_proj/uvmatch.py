import maya.cmds as cmds
def moveToVert(index):
	ctrl = "animMorph_body_proxy.vtx[" + str(index) + "]"
	fol = cmds.ls(selection = True)[0]
	folShape = fol[:-4] + "Shape" + fol[-4:]
	position = cmds.xform(ctrl, query = True, translation = True, worldSpace = True)
	cmds.setAttr("closestPointOnMesh1.inPosition.inPositionX", position[0])
	cmds.setAttr("closestPointOnMesh1.inPosition.inPositionY", position[1])
	cmds.setAttr("closestPointOnMesh1.inPosition.inPositionZ", position[2])
	u = cmds.getAttr("closestPointOnMesh1.result.parameterU")
	v = cmds.getAttr("closestPointOnMesh1.result.parameterV")
	cmds.setAttr(folShape + ".parameterU", u)
	cmds.setAttr(folShape + ".parameterV", v)