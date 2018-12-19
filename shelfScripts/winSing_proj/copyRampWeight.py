clstr = cmds.ls(selection = True)[0]
for i in xrange(20):
    weight = cmds.getAttr("anim_mouth_upperLip_curv_clustrCluster.weightList[0].weights[" + str(i) + "]")
    cmds.setAttr(clstr + "Cluster.weightList[0].weights[" + str(i) + "]", weight)

clstr = cmds.ls(selection = True)[0]
for i in xrange(20):
    weight = cmds.getAttr("anim_mouth_lowerLip_curv_clustrCluster.weightList[0].weights[" + str(i) + "]")
    cmds.setAttr(clstr + "Cluster.weightList[0].weights[" + str(i) + "]", weight)