import maya.cmds as cmds
fromJntLs = [u'anim_l_leg_femurFix_y_neg_z_bn', u'anim_l_leg_femurFix_z_neg_y_neg_2_bn', u'anim_l_leg_femurFix_y_neg_y_bn', u'anim_l_leg_femurFix_z_y_2_bn', u'anim_l_leg_femurFix_y_neg_y_neg_bn', u'anim_l_leg_femurFix_z_neg_y_neg_bn', u'anim_l_leg_femurFix_z_neg_x_neg_bn', u'anim_l_leg_femurFix_z_neg_x_neg_2_bn', u'anim_l_leg_femurFix_z_y_bn', u'anim_l_leg_femurFix_z_y_3_bn', u'anim_l_leg_femurFix_z_x_neg_bn', u'anim_l_leg_femurFix_z_z_neg_bn']
toJntLs = [u'anim_r_leg_femurFix_y_neg_z_bn', u'anim_r_leg_femurFix_z_neg_y_neg_2_bn', u'anim_r_leg_femurFix_y_neg_y_bn', u'anim_r_leg_femurFix_z_y_2_bn', u'anim_r_leg_femurFix_y_neg_y_neg_bn', u'anim_r_leg_femurFix_z_neg_y_neg_bn', u'anim_r_leg_femurFix_z_neg_x_neg_bn', u'anim_r_leg_femurFix_z_neg_x_neg_2_bn', u'anim_r_leg_femurFix_z_y_bn', u'anim_r_leg_femurFix_z_y_3_bn', u'anim_r_leg_femurFix_z_x_neg_bn', u'anim_r_leg_femurFix_z_z_neg_bn'] # 
fromJntLs += ["anim_l_leg_rot_root_bn"]
toJntLs += ["anim_r_leg_rot_root_bn"]
indexLs = [118, 120, 129, 124, 119, 130, 121, 122, 123, 125, 126, 131, 101]
fromLs = [u'body_new.vtx[1625]', u'body_new.vtx[1626]', u'body_new.vtx[1628]', u'body_new.vtx[1629]', u'body_new.vtx[1630]', u'body_new.vtx[1631]', u'body_new.vtx[1632]', u'body_new.vtx[1633]', u'body_new.vtx[1634]', u'body_new.vtx[1635]', u'body_new.vtx[1636]', u'body_new.vtx[1637]', u'body_new.vtx[1638]', u'body_new.vtx[1639]', u'body_new.vtx[1640]', u'body_new.vtx[1641]', u'body_new.vtx[1642]', u'body_new.vtx[1643]', u'body_new.vtx[1644]', u'body_new.vtx[1645]', u'body_new.vtx[1646]', u'body_new.vtx[1647]', u'body_new.vtx[1648]', u'body_new.vtx[1649]', u'body_new.vtx[1650]', u'body_new.vtx[1651]', u'body_new.vtx[1652]', u'body_new.vtx[1653]', u'body_new.vtx[1654]', u'body_new.vtx[1655]', u'body_new.vtx[1656]', u'body_new.vtx[1657]', u'body_new.vtx[1658]', u'body_new.vtx[1659]', u'body_new.vtx[1660]', u'body_new.vtx[1661]', u'body_new.vtx[1662]', u'body_new.vtx[1663]', u'body_new.vtx[1664]', u'body_new.vtx[1665]', u'body_new.vtx[1666]', u'body_new.vtx[1667]', u'body_new.vtx[1668]', u'body_new.vtx[1669]', u'body_new.vtx[1670]', u'body_new.vtx[1671]', u'body_new.vtx[1672]', u'body_new.vtx[1673]', u'body_new.vtx[1674]', u'body_new.vtx[1675]', u'body_new.vtx[1676]', u'body_new.vtx[1677]', u'body_new.vtx[1678]', u'body_new.vtx[1679]', u'body_new.vtx[1680]', u'body_new.vtx[1681]', u'body_new.vtx[1682]', u'body_new.vtx[1683]', u'body_new.vtx[1684]', u'body_new.vtx[1685]', u'body_new.vtx[1686]', u'body_new.vtx[1687]', u'body_new.vtx[1688]', u'body_new.vtx[1689]', u'body_new.vtx[1690]', u'body_new.vtx[1691]', u'body_new.vtx[1692]', u'body_new.vtx[1693]', u'body_new.vtx[1694]', u'body_new.vtx[1695]', u'body_new.vtx[1696]', u'body_new.vtx[1697]', u'body_new.vtx[1698]', u'body_new.vtx[1699]', u'body_new.vtx[1700]', u'body_new.vtx[1701]', u'body_new.vtx[1702]', u'body_new.vtx[1703]', u'body_new.vtx[1704]', u'body_new.vtx[1705]', u'body_new.vtx[1706]', u'body_new.vtx[1707]', u'body_new.vtx[1708]', u'body_new.vtx[1709]', u'body_new.vtx[1710]', u'body_new.vtx[1711]', u'body_new.vtx[1712]', u'body_new.vtx[1713]', u'body_new.vtx[1714]', u'body_new.vtx[1715]', u'body_new.vtx[1716]', u'body_new.vtx[1717]', u'body_new.vtx[1718]', u'body_new.vtx[1719]', u'body_new.vtx[1720]', u'body_new.vtx[1721]', u'body_new.vtx[1722]', u'body_new.vtx[1723]', u'body_new.vtx[1724]', u'body_new.vtx[1725]', u'body_new.vtx[1729]', u'body_new.vtx[1752]', u'body_new.vtx[1901]', u'body_new.vtx[1902]', u'body_new.vtx[1903]', u'body_new.vtx[1904]', u'body_new.vtx[1905]', u'body_new.vtx[1959]', u'body_new.vtx[1968]', u'body_new.vtx[1969]', u'body_new.vtx[1970]', u'body_new.vtx[1971]', u'body_new.vtx[1981]', u'body_new.vtx[1982]', u'body_new.vtx[1983]', u'body_new.vtx[1984]', u'body_new.vtx[1992]', u'body_new.vtx[1993]', u'body_new.vtx[1994]', u'body_new.vtx[1995]', u'body_new.vtx[1996]', u'body_new.vtx[1997]', u'body_new.vtx[1998]', u'body_new.vtx[1999]', u'body_new.vtx[2009]', u'body_new.vtx[2010]', u'body_new.vtx[2011]', u'body_new.vtx[2012]', u'body_new.vtx[2068]', u'body_new.vtx[2069]', u'body_new.vtx[2070]', u'body_new.vtx[2071]', u'body_new.vtx[2113]', u'body_new.vtx[2114]', u'body_new.vtx[2115]', u'body_new.vtx[2116]', u'body_new.vtx[2117]', u'body_new.vtx[2118]', u'body_new.vtx[2119]', u'body_new.vtx[2120]', u'body_new.vtx[2123]', u'body_new.vtx[2124]', u'body_new.vtx[2125]', u'body_new.vtx[2126]', u'body_new.vtx[2127]', u'body_new.vtx[2128]', u'body_new.vtx[2129]', u'body_new.vtx[2130]', u'body_new.vtx[2133]', u'body_new.vtx[2134]', u'body_new.vtx[2135]', u'body_new.vtx[2136]', u'body_new.vtx[2137]', u'body_new.vtx[2435]', u'body_new.vtx[2436]', u'body_new.vtx[2437]', u'body_new.vtx[2438]', u'body_new.vtx[2439]', u'body_new.vtx[2440]', u'body_new.vtx[2441]', u'body_new.vtx[2442]', u'body_new.vtx[2443]', u'body_new.vtx[2444]', u'body_new.vtx[2445]', u'body_new.vtx[2446]', u'body_new.vtx[2447]', u'body_new.vtx[2448]', u'body_new.vtx[2449]', u'body_new.vtx[2450]', u'body_new.vtx[2451]', u'body_new.vtx[2452]', u'body_new.vtx[2458]', u'body_new.vtx[2460]', u'body_new.vtx[2461]', u'body_new.vtx[2462]', u'body_new.vtx[2463]', u'body_new.vtx[2464]', u'body_new.vtx[2465]', u'body_new.vtx[2466]', u'body_new.vtx[2467]', u'body_new.vtx[2468]', u'body_new.vtx[2469]', u'body_new.vtx[2470]', u'body_new.vtx[2471]', u'body_new.vtx[2472]', u'body_new.vtx[2473]', u'body_new.vtx[2474]', u'body_new.vtx[2477]', u'body_new.vtx[2478]', u'body_new.vtx[2481]', u'body_new.vtx[2487]', u'body_new.vtx[2488]', u'body_new.vtx[2491]', u'body_new.vtx[2492]', u'body_new.vtx[2508]', u'body_new.vtx[2509]', u'body_new.vtx[2519]', u'body_new.vtx[2520]', u'body_new.vtx[2521]', u'body_new.vtx[2524]', u'body_new.vtx[2525]', u'body_new.vtx[2526]', u'body_new.vtx[2527]', u'body_new.vtx[2528]', u'body_new.vtx[2529]', u'body_new.vtx[2530]', u'body_new.vtx[2531]', u'body_new.vtx[2532]', u'body_new.vtx[2533]', u'body_new.vtx[2534]', u'body_new.vtx[2535]', u'body_new.vtx[2536]', u'body_new.vtx[2537]', u'body_new.vtx[2538]', u'body_new.vtx[2539]', u'body_new.vtx[2540]', u'body_new.vtx[2541]', u'body_new.vtx[2542]', u'body_new.vtx[2543]', u'body_new.vtx[2547]', u'body_new.vtx[2548]', u'body_new.vtx[2549]', u'body_new.vtx[2550]', u'body_new.vtx[2552]', u'body_new.vtx[2554]', u'body_new.vtx[2555]', u'body_new.vtx[2556]', u'body_new.vtx[2557]', u'body_new.vtx[2558]', u'body_new.vtx[2559]', u'body_new.vtx[2560]', u'body_new.vtx[2561]', u'body_new.vtx[2562]', u'body_new.vtx[2563]', u'body_new.vtx[2564]', u'body_new.vtx[2926]', u'body_new.vtx[2927]', u'body_new.vtx[2928]', u'body_new.vtx[2929]', u'body_new.vtx[2930]', u'body_new.vtx[2931]', u'body_new.vtx[2932]', u'body_new.vtx[2934]', u'body_new.vtx[2935]', u'body_new.vtx[2936]', u'body_new.vtx[2937]', u'body_new.vtx[2939]', u'body_new.vtx[2940]', u'body_new.vtx[2941]', u'body_new.vtx[2942]', u'body_new.vtx[2943]', u'body_new.vtx[2944]', u'body_new.vtx[2945]', u'body_new.vtx[2946]', u'body_new.vtx[2947]', u'body_new.vtx[2950]', u'body_new.vtx[2951]', u'body_new.vtx[2952]', u'body_new.vtx[2953]', u'body_new.vtx[2954]', u'body_new.vtx[2955]', u'body_new.vtx[2956]', u'body_new.vtx[2957]', u'body_new.vtx[2958]', u'body_new.vtx[2959]', u'body_new.vtx[2960]', u'body_new.vtx[2961]', u'body_new.vtx[2962]', u'body_new.vtx[2963]', u'body_new.vtx[2964]', u'body_new.vtx[2965]', u'body_new.vtx[2966]', u'body_new.vtx[2967]', u'body_new.vtx[2968]', u'body_new.vtx[2969]', u'body_new.vtx[2970]', u'body_new.vtx[2971]', u'body_new.vtx[2972]', u'body_new.vtx[2975]', u'body_new.vtx[2976]', u'body_new.vtx[2977]', u'body_new.vtx[2979]', u'body_new.vtx[2991]', u'body_new.vtx[2992]', u'body_new.vtx[2993]', u'body_new.vtx[2994]', u'body_new.vtx[2996]', u'body_new.vtx[2997]', u'body_new.vtx[7845]', u'body_new.vtx[7846]', u'body_new.vtx[7847]', u'body_new.vtx[7848]', u'body_new.vtx[7849]']




def getWeight(vtx, fromJntLs):
	weightLs = []
	for jnt in fromJntLs:
		weightLs += [cmds.skinPercent("skinCluster18", vtx, query = True, transform = jnt)]
	return weightLs

def setWeight(vtx, weightLs):
	oldWeightLs = []
	oldWeightSum = 0
	jntLs = cmds.skinPercent("skinCluster18", vtx, query = True, transform = None)
	valueLs = cmds.skinPercent("skinCluster18", vtx, query = True, value = True)
	for jnt in toJntLs:
		oldWeightSum += crtWeight
	weightLs[-1] = oldWeightSum - sum(weightLs[:-1])
	for i in xrange(len(fromJntLs)):
		valueLs[indexLs[i]] = weightLs[i]
	tvLs = []
	for i in xrange(len(valueLs)):
		tvLs += [(jntLs[i], valueLs[i])]
	cmds.skinPercent("skinCluster18", vtx, transformValue = tvLs)


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
	weightLs = getWeight(fromVtx, fromJntLs)
	setWeight(toVtx, weightLs)