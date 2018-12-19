import maya.cmds as cmds

def getWeight(vtx):
	return (cmds.skinPercent("skinCluster18", vtx, query = True, transform = "anim_l_arm_elbowFix_y_trans_bn"))

def setWeight(vtx, weight):
	jntLs = cmds.skinPercent("skinCluster18", vtx, query = True, transform = None)
	valueLs = cmds.skinPercent("skinCluster18", vtx, query = True, value = True)
	wristWeight = cmds.skinPercent("skinCluster18", vtx, query = True, transform = "anim_r_arm_lower_rot_root_bn")
	newWristWeight = wristWeight - weight
	valueLs[128] = newWristWeight
	valueLs[116] = weight
	tvLs = []
	for i in xrange(len(valueLs)):
		tvLs += [(jntLs[i], valueLs[i])]
	cmds.skinPercent("skinCluster18", vtx, transformValue = tvLs)
fromLs = [u'body_new.vtx[2177]', u'body_new.vtx[2178]', u'body_new.vtx[2181]', u'body_new.vtx[2182]', u'body_new.vtx[2184]', u'body_new.vtx[2186]', u'body_new.vtx[2189]', u'body_new.vtx[2190]', u'body_new.vtx[2192]', u'body_new.vtx[2194]', u'body_new.vtx[2196]', u'body_new.vtx[2198]', u'body_new.vtx[2199]', u'body_new.vtx[2202]', u'body_new.vtx[2204]', u'body_new.vtx[2206]', u'body_new.vtx[2208]', u'body_new.vtx[2209]', u'body_new.vtx[2211]', u'body_new.vtx[2212]', u'body_new.vtx[2213]', u'body_new.vtx[2214]', u'body_new.vtx[2215]', u'body_new.vtx[2216]', u'body_new.vtx[2217]', u'body_new.vtx[2218]', u'body_new.vtx[2219]', u'body_new.vtx[2220]', u'body_new.vtx[2221]', u'body_new.vtx[2222]', u'body_new.vtx[2223]', u'body_new.vtx[2224]', u'body_new.vtx[2225]', u'body_new.vtx[2226]', u'body_new.vtx[2229]', u'body_new.vtx[2230]', u'body_new.vtx[2232]', u'body_new.vtx[2233]', u'body_new.vtx[2236]', u'body_new.vtx[2237]', u'body_new.vtx[2238]', u'body_new.vtx[2239]', u'body_new.vtx[2240]', u'body_new.vtx[2241]', u'body_new.vtx[2242]', u'body_new.vtx[2243]', u'body_new.vtx[2244]', u'body_new.vtx[2245]', u'body_new.vtx[2246]', u'body_new.vtx[2247]', u'body_new.vtx[2248]', u'body_new.vtx[2249]', u'body_new.vtx[2250]', u'body_new.vtx[2331]', u'body_new.vtx[2332]', u'body_new.vtx[2333]', u'body_new.vtx[2334]', u'body_new.vtx[2335]', u'body_new.vtx[2336]', u'body_new.vtx[2337]', u'body_new.vtx[2338]', u'body_new.vtx[2339]', u'body_new.vtx[2340]', u'body_new.vtx[2341]', u'body_new.vtx[2342]', u'body_new.vtx[2343]', u'body_new.vtx[2344]', u'body_new.vtx[2345]', u'body_new.vtx[2346]', u'body_new.vtx[2347]', u'body_new.vtx[2348]', u'body_new.vtx[2349]', u'body_new.vtx[2350]']
for i in xrange(len(fromLs)):
	cmds.select(fromLs[i], sym = True)
	allVtxLs = cmds.ls(selection = True)
	vtx1 = allVtxLs[0]
	vtx2 = allVtxLs[1]
	vtx1Index = int(vtx1[13:-1])
	vtx2Index = int(vtx1[13:-1])
	if vtx1Index > vtx2Index:
		fromVtx = vtx2
		toVtx = vtx1
	else:
		fromVtx = vtx1
		toVtx = vtx2
	print "from: " + fromVtx
	print "to: " + toVtx
	weight = getWeight(fromVtx)
	setWeight(toVtx, weight)