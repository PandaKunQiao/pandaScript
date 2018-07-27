import maya.cmds as cmds

vtxLs = cmds.ls(selection = True, flatten = True)
MIRRORVTXLS = []
jntLs = cmds.skinPercent("skinCluster1", "body.vtx[1]", query = True, transform = None)
spineIndex = jntLs.index("morph_spine_1_jnt")
hipIndex = jntLs.index("morph_l_b_hip_jnt")
rootIndex = jntLs.index("temproot")
gwsIndex = jntLs.index("morph_l_b_hip_goWithSpine_jnt")
for vtx in  vtxLs:
	print vtx
	origPos = cmds.xform(vtx, query = True, translation = True, worldSpace = True)
	mirrorPos = [-origPos[0], origPos[1], origPos[2]]
	cmds.setAttr("closestPointOnMesh_buttHelp.inPosition", mirrorPos[0], mirrorPos[1], mirrorPos[2], type = "double3")
	vtxIndex = cmds.getAttr("closestPointOnMesh_buttHelp.result.closestVertexIndex")
	mirrorVtx = "body.vtx[" + str(vtxIndex) + "]"
	spineWeight = cmds.skinPercent("skinCluster1", mirrorVtx, query = True, transform = "morph_spine_1_jnt")
	hipWeight = cmds.skinPercent("skinCluster1", vtx, query = True, transform = "morph_l_b_hip_jnt")
	temproot = cmds.skinPercent("skinCluster1", mirrorVtx, query = True, transform = "temproot")
	newHipWeight = 0
	newTemproot = 0
	newSpineWeight = 0
	gwsWeight = 0
	if (hipWeight <= temproot):
		print "a"
		newHipWeight = hipWeight
		newTemproot = temproot - newHipWeight
		newSpineWeight = spineWeight
		gwsWeight = 0
	else:
		print "b"
		newHipWeight = temproot
		newTemproot = 0
		gwsWeight = hipWeight - newHipWeight
		newSpineWeight = spineWeight - gwsWeight

	valueLs = cmds.skinPercent("skinCluster1", vtx, query = True, value = True)
	tvLs = []
	for i in xrange(len(jntLs)):
		tvLs += [(jntLs[i], valueLs[i])]
	print newHipWeight
	print newTemproot
	print newSpineWeight
	print gwsWeight
	tvLs[spineIndex] = (jntLs[spineIndex], newSpineWeight)
	tvLs[hipIndex] = (jntLs[hipIndex], newHipWeight)
	tvLs[rootIndex] = (jntLs[rootIndex], newTemproot)
	tvLs[gwsIndex] = (jntLs[gwsIndex], gwsWeight)
	MIRRORVTXLS += [mirrorVtx]
	cmds.skinPercent("skinCluster1", vtx, transformValue = tvLs)