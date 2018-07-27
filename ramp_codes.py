# import maya.cmds as cmds

# for loop to create expression
# for i in xrange(46):
# 	print "morph_spine_main_clstrCluster.weightList[0].weights[" + str(i) + "] = $output[" + str(i) + "];"
for i in xrange(9):
 	print "morph_spine_" + str(i+1) + "_jnt.scaleY = $output[" + str(i) + "];"
 	print "morph_spine_" + str(i+1) + "_jnt.scaleZ = $output[" + str(i) + "];"

/*
*/
vector $dummy = morph_spine_ramp.outAlpha;
float $output[];
float $offset = 1.0/45.0*2.5;
float $gap = (1.0 - $offset * 2)/5.0;
for ($i = 0; $i<= 5; $i++){
	float $pos = $i * $gap + $offset;
	float $val[] = `colorAtPoint -u 0.5 -v $pos morph_spine_ramp`;
	$output[$i] = 1 + $val[0] * ctrl_scale.spine_scale;
}
morph_belly_1_jnt.scaleY = $output[0];
morph_belly_1_jnt.scaleZ = $output[0];
morph_belly_2_jnt.scaleY = $output[1];
morph_belly_2_jnt.scaleZ = $output[1];
morph_belly_3_jnt.scaleY = $output[2];
morph_belly_3_jnt.scaleZ = $output[2];
morph_belly_4_jnt.scaleY = $output[3];
morph_belly_4_jnt.scaleZ = $output[3];
morph_belly_5_jnt.scaleY = $output[4];
morph_belly_5_jnt.scaleZ = $output[4];
morph_belly_6_jnt.scaleY = $output[5];
morph_belly_6_jnt.scaleZ = $output[5];