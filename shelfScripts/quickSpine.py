import maya.cmds as cmds
SPINEJNTCHAIN = ["sk_spine_root_jnt", "sk_spineA_jnt", "sk_spineB_jnt", "sk_spine_end_jnt"]
IKSPINEHANDLE = "ikspine_ikhandle"
IKSPINECURVE = "ikspine_curve"
IKSPINEHANDLECHAIN = ["ikspine_clutr_1_clstr", "ikspine_clstr_2_clstr", 
					  "ikspine_clstr_3_clstr", "ikspine_clstr_4_clstr", 
					  "ikspine_clstr_5_clstr", "ikspine_clstr_6_clstr"]
IKSPINECTRLCHAIN = ["ctrl_hips" ,"ctrl_fk_spine_A" ,"ctrl_midspine" ,"ctrl_fk_spine_B" ,"ctrl_chest"]
CHESTJNT = "sk_chest_jnt"
HIPSJNT = "sk_hips_jnt"


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


# input: the satrt joint (root), the end joint
# out put: curve corresponding to the ikspine
# side effects: create ik spine and name it correctly
def createIkSpine(startEff, endEff):
	[ikhandle, eff, crv] = cmds.ikHandle(startJoint = startEff, endEffector = endEff, solver = "ikSplineSolver", simplifyCurve = False)
	ikhandle = cmds.rename(ikhandle, IKSPINEHANDLE)
	crv = cmds.rename(crv, IKSPINECURVE)
	# cmds.setAttr()
	return crv

# input: the curve 
# output: cluster list corresponding to the curve
# side effect: create cluster deformer for each cv of the curve
def clustrIkCrv(curve):
	cvNum = cmds.getAttr(curve + ".spans") + cmds.getAttr(curve + ".degree")
	handleList = []
	for i in xrange(cvNum):
		cv = curve + ".cv[" + str(i) + "]"
		[handle, clstr] = cmds.cluster(cv)
		print clstr
		handle = cmds.rename(clstr, IKSPINEHANDLECHAIN[i])
		handleList += [handle]
	print handleList
	return handleList

# input: the joint list, cluster handle list, control list
# output:
# side effect:
def createIkSpineCtrls(jntLs, handleLs, ctrlLs, chestJnt, hipsJnt):

	# create the first control at root joint
	hipsCtrl = cmds.circle(name = ctrlLs[0], nr = [0, 1, 0])[0]
	refHipsCtrl = cmds.createNode("transform", name = "ref_" + ctrlLs[0])
	cmds.parent(hipsCtrl, refHipsCtrl)
	posHips = cmds.xform(jntLs[0], query = True, worldSpace = True, translation = True)
	cmds.xform(refHipsCtrl, translation = posHips, worldSpace = True)

	# create the chest control at chest joint
	chestCtrl = cmds.circle(name = ctrlLs[-1], nr = [0, 1, 0])[0]
	refChestCtrl = cmds.createNode("transform", name = "ref_" + ctrlLs[-1])
	cmds.parent(chestCtrl, refChestCtrl)
	posChest = cmds.xform(jntLs[-1], query = True, worldSpace = True, translation = True)
	cmds.xform(refChestCtrl, translation = posChest, worldSpace = True)

	# create the midSpine control in the middle
	midSpineCtrl = cmds.circle(name = ctrlLs[2], nr = [0, 1, 0])[0]
	refMidSpineCtrl = cmds.createNode("transform", name = "ref_" + ctrlLs[2])
	cmds.parent(midSpineCtrl, refMidSpineCtrl)
	posMidSpine = [(posChest[0] + posHips[0])/2.0, 
				   (posChest[1] + posHips[1])/2.0, 
				   (posChest[2] + posHips[2])/2.0]
	cmds.xform(refMidSpineCtrl, translation = posMidSpine, worldSpace = True)

	# create the spine_A control in the middle
	spineACtrl = cmds.circle(name = ctrlLs[1], nr = [0, 1, 0])[0]
	refSpineACtrl = cmds.createNode("transform", name = "ref_" + ctrlLs[1])
	cmds.parent(spineACtrl, refSpineACtrl)
	posSpineA = [(posMidSpine[0] + posHips[0])/2.0, 
				 (posMidSpine[1] + posHips[1])/2.0, 
				 (posMidSpine[2] + posHips[2])/2.0]
	cmds.xform(refSpineACtrl, translation = posSpineA, worldSpace = True)

	# create the spine_B control in the middle
	spineBCtrl = cmds.circle(name = ctrlLs[3], nr = [0, 1, 0])[0]
	refSpineBCtrl = cmds.createNode("transform", name = "ref_" + ctrlLs[3])
	cmds.parent(spineBCtrl, refSpineBCtrl)
	posSpineB = [(posMidSpine[0] + posChest[0])/2.0, 
				 (posMidSpine[1] + posChest[1])/2.0, 
				 (posMidSpine[2] + posChest[2])/2.0]
	cmds.xform(refSpineBCtrl, translation = posSpineB, worldSpace = True)


	# do parent constraints to handles
	cmds.parentConstraint(hipsCtrl, handleLs[0], maintainOffset = True)
	cmds.parentConstraint(hipsCtrl, handleLs[1], maintainOffset = True)

	cmds.parentConstraint(hipsCtrl, midSpineCtrl, handleLs[2], maintainOffset = True)
	cmds.parentConstraint(chestCtrl, midSpineCtrl, handleLs[3], maintainOffset = True)

	cmds.parentConstraint(chestCtrl, handleLs[4], maintainOffset = True)
	cmds.parentConstraint(chestCtrl, handleLs[5], maintainOffset = True)

	# do parent constraint to joints
	cmds.parentConstraint(chestCtrl, chestJnt, maintainOffset = True)
	cmds.parentConstraint(hipsCtrl, hipsJnt, maintainOffset = True)

	# put chain in the right order
	cmds.parent(refChestCtrl, spineBCtrl)
	cmds.parent(refSpineBCtrl, spineACtrl)
	cmds.parent(refMidSpineCtrl, spineACtrl)
spineCrv = createIkSpine(SPINEJNTCHAIN[0], SPINEJNTCHAIN[-1])
spineHandleLs = clustrIkCrv(spineCrv)
createIkSpineCtrls(SPINEJNTCHAIN, spineHandleLs, IKSPINECTRLCHAIN, CHESTJNT, HIPSJNT)