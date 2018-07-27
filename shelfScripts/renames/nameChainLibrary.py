# for arm controls
ARMJNTCHAIN = ["sk_l_shoulder_jnt", "sk_l_elbow_jnt", "sk_l_wrist_jnt"]
IKARMJNTCHAIN = ["ik_l_shoulder_jnt" ,"ik_l_elbow_jnt" ,"ik_l_wrist_jnt"]
FKARMJNTCHAIN = ["fk_l_shoulder_jnt" ,"fk_l_elbow_jnt" ,"fk_l_wrist_jnt"]
IKARMCTRLCHAIN = ["ctrl_l_ik_elbow" ,"ctrl_l_ik_wrist"]
FKARMCTRLCHAIN = ["ctrl_l_fk_shoulder" ,"ctrl_l_fk_elbow" ,"ctrl_l_fk_wrist"]
ARMSWITCHCTRL = "ctrl_l_armSwitch"
HANDCTRL = "ctrl_l_hand"
REVARMNODE = "rev_l_arm"



# non flip system
UPPERARMTWISTCHAIN = ["twist_l_upperArm_start_jnt" "twist_l_upperArm_1_jnt", 
					  "twist_l_upperArm_2_jnt", "twist_l_upperArm_3_jnt", 
					  "twist_l_upperArm_end_jnt"]





# for finger controls

FINGERJNTCHAIN ["sk_l_thumb_A_jnt" ,"sk_l_thumb_B_jnt" ,"sk_l_thumb_C_jnt",
				"sk_l_index_A_jnt" ,"sk_l_index_B_jnt" ,"sk_l_index_C_jnt" ,
				"sk_l_middle_A_jnt" ,"sk_l_middle_B_jnt" ,"sk_l_middle_C_jnt" ,
				"sk_l_ring_A_jnt" ,"sk_l_ring_B_jnt" ,"sk_l_ring_C_jnt" ,
				"sk_l_little_A_jnt" ,"sk_l_little_B_jnt" ,"sk_l_little_C_jnt"]

THUMBJNTCHAIN = 	["sk_l_thumb_A", "sk_l_thumb_B", "sk_l_thumb_C"]
INDEXJNTCHAIN = 	["sk_l_index_A", "sk_l_index_B", "sk_l_index_C"]
MIDDLEJNTCHAIN = 	["sk_l_middle_A", "sk_l_middle_B", "sk_l_middle_C"]
RINGJNTCHAIN = 	["sk_l_ring_A", "sk_l_ring_B", "sk_l_ring_C"]
LITTLEJNTCHAIN = 	["sk_l_little_A", "sk_l_little_B", "sk_l_little_C"]

PALMJNT = "sk_l_palm_jnt"

FINGERCTRLCHAIN = ["ctrl_l_thumb_A", "ctrl_l_thumb_B", "ctrl_l_thumb_C", 
					"ctrl_l_index_A", "ctrl_l_index_B", "ctrl_l_index_C", 
					"ctrl_l_middle_A", "ctrl_l_middle_B", "ctrl_l_middle_C", 
					"ctrl_l_ring_A", "ctrl_l_ring_B", "ctrl_l_ring_C", 
					"ctrl_l_little_A", "ctrl_l_little_B", "ctrl_l_little_C"]

THUMBCTRLCHAIN = 	["ctrl_l_thumb_A", "ctrl_l_thumb_B", "ctrl_l_thumb_C"]
INDEXCTRLCHAIN = 	["ctrl_l_index_A", "ctrl_l_index_B", "ctrl_l_index_C"]
MIDDLECTRLCHAIN = 	["ctrl_l_middle_A", "ctrl_l_middle_B", "ctrl_l_middle_C"]
RINGCTRLCHAIN = 	["ctrl_l_ring_A", "ctrl_l_ring_B", "ctrl_l_ring_C"]
LITTLECTRLCHAIN = 	["ctrl_l_little_A", "ctrl_l_little_B", "ctrl_l_little_C"]

FINGERORIGCTRL = "finger_original_ctrl"
PALMCTRL = "ctrl_l_palm"


# assisting cube names
HANDCUBE = "cube_l_hand"
THUMBCUBE = "cube_l_thumb"
INDEXCUBE = "cube_l_index"
MIDDLECUBE = "cube_l_middle"
RINGCUBE = "cube_l_ring"
LITTLECUBE = "cube_l_little"

FINGERATTRLS = [("custom_attributes", "enum", ("_________", 0)),
				("fist", "float", 0),
				("neutral"， "float", 0),
				("claw", "float", 0),
				("bind", "float", 0)]

# right side
# for arm controls
ARMJNTCHAIN_R = ["sk_r_shoulder_jnt", "sk_r_elbow_jnt", "sk_r_wrist_jnt"]
IKARMJNTCHAIN_R = ["ik_r_shoulder_jnt" ,"ik_r_elbow_jnt" ,"ik_r_wrist_jnt"]
FKARMJNTCHAIN_R = ["fk_r_shoulder_jnt" ,"fk_r_elbow_jnt" ,"fk_r_wrist_jnt"]
IKARMCTRLCHAIN_R = ["ctrl_r_ik_elbow" ,"ctrl_r_ik_wrist"]
FKARMCTRLCHAIN_R = ["ctrl_r_fk_shoulder" ,"ctrl_r_fk_elbow" ,"ctrl_r_fk_wrist"]
FKIKSWITCHCTRL_R = "ctrl_r_armSwitch"
HANDCTRL_R = "ctrl_r_hand"
REVARMNODE_R = "rev_r_arm"
FINGERATTRLS_R = [("custom_attributes", "enum", ("_________", 0)),
				("fist", "float", 0),
				("neutral", "float", 0),
				("claw", "float", 0),
				("bind", "float", 0)]

FINGERREFCHAIN_R = ["ref_ctrl_r_thumb_A", "ref_ctrl_r_thumb_B", "ref_ctrl_r_thumb_C", 
					"ref_ctrl_r_index_A", "ref_ctrl_r_index_B", "ref_ctrl_r_index_C", 
					"ref_ctrl_r_middle_A", "ref_ctrl_r_middle_B", "ref_ctrl_r_middle_C", 
					"ref_ctrl_r_ring_A", "ref_ctrl_r_ring_B", "ref_ctrl_r_ring_C", 
					"ref_ctrl_r_little_A", "ref_ctrl_r_little_B", "ref_ctrl_r_little_C"]

FINGERCTRLCHAIN_R = ["ctrl_r_thumb_A", "ctrl_r_thumb_B", "ctrl_r_thumb_C", 
					"ctrl_r_index_A", "ctrl_r_index_B", "ctrl_r_index_C", 
					"ctrl_r_middle_A", "ctrl_r_middle_B", "ctrl_r_middle_C", 
					"ctrl_r_ring_A", "ctrl_r_ring_B", "ctrl_r_ring_C", 
					"ctrl_r_little_A", "ctrl_r_little_B", "ctrl_r_little_C"]

THUMBCTRLCHAIN_R = 	["ctrl_r_thumb_A", "ctrl_r_thumb_B", "ctrl_r_thumb_C"]
INDEXCTRLCHAIN_R = 	["ctrl_r_index_A", "ctrl_r_index_B", "ctrl_r_index_C"]
MIDDLECTRLCHAIN_R = 	["ctrl_r_middle_A", "ctrl_r_middle_B", "ctrl_r_middle_C"]
RINGCTRLCHAIN_R = 	["ctrl_r_ring_A", "ctrl_r_ring_B", "ctrl_r_ring_C"]
LITTLECTRLCHAIN_R = 	["ctrl_r_little_A", "ctrl_r_little_B", "ctrl_r_little_C"]

FINGERJNTCHAIN_R = ["sk_r_thumb_A_jnt" ,"sk_r_thumb_B_jnt" ,"sk_r_thumb_C_jnt",
				  "sk_r_index_A_jnt" ,"sk_r_index_B_jnt" ,"sk_r_index_C_jnt" ,
				  "sk_r_middle_A_jnt" ,"sk_r_middle_B_jnt" ,"sk_r_middle_C_jnt" ,
				  "sk_r_ring_A_jnt" ,"sk_r_ring_B_jnt" ,"sk_r_ring_C_jnt" ,
				  "sk_r_little_A_jnt" ,"sk_r_little_B_jnt" ,"sk_r_little_C_jnt"]



# for foot controls
LEGJNTCHAIN = ["sk_l_femur_jnt" ,"sk_l_knee_jnt" ,"sk_l_ankle_jnt" ,"sk_l_ball_jnt" ,"sk_l_toe_jnt"]
IKLEGJNTCHAIN = ["ik_l_femur_jnt" ,"ik_l_knee_jnt" ,"ik_l_ankle_jnt"]
FKLEGJNTCHAIN = ["fk_l_femur_jnt" ,"fk_l_knee_jnt" ,"fk_l_ankle_jnt"]

LEGFKCTRLCHAIN = ["ctrl_l_fk_femur" ,"ctrl_l_fk_knee" ,"ctrl_l_fk_ankle"]
LEGIKCTRLCHAIN = ["ctrl_l_knee" ,"ctrl_l_ik_foot"]

LEGSWITCHCTRL = "ctrl_l_legSwitch"
LEGSWITCHATTR = "ik_leg"
REVLEGNODE = "rev_l_leg"



REVERSEFOOTJNTCHAIN = ["rf_l_outFoot_jnt", "rf_l_inFoot_jnt", "rf_l_heel_jnt", "rf_l_toe_jnt", "rf_l_ball_jnt", "rf_l_ankle_jnt"]
REVERSEFOOTIKHANDLECHAIN = ["ikleg_l_ankle_ikhandle" ,"rf_l_ball_ikhandle" ,"rf_l_toe_ikhandle"]


# on the right side 
LEGJNTCHAIN_R = ["sk_r_femur_jnt" ,"sk_r_knee_jnt" ,"sk_r_ankle_jnt" ,"sk_r_ball_jnt" ,"sk_r_toe_jnt"]
IKLEGJNTCHAIN_R = ["ik_r_femur_jnt" ,"ik_r_knee_jnt" ,"ik_r_ankle_jnt"]
FKLEGJNTCHAIN_R = ["fk_r_femur_jnt" ,"fk_r_knee_jnt" ,"fk_r_ankle_jnt"]

LEGFKCTRLCHAIN_R = ["ctrl_r_fk_femur" ,"ctrl_r_fk_knee" ,"ctrl_r_fk_ankle"]
LEGIKCTRLCHAIN_R = ["ctrl_r_knee" ,"ctrl_r_ik_foot"]

LEGSWITCHCTRL_R = "ctrl_r_legSwitch"
REVLEGNODE_R = "rev_r_leg"

REVERSEFOOTJNTCHAIN_R = ["rf_r_outFoot_jnt", "rf_r_inFoot_jnt", "rf_r_heel_jnt", "rf_r_toe_jnt", "rf_r_ball_jnt", "rf_r_ankle_jnt"]
REVERSEFOOTIKHANDLECHAIN_R = ["ikleg_r_ankle_ikhandle" ,"rf_r_ball_ikhandle" ,"rf_r_toe_ikhandle"]

RFATTRLS = [("custom_attributes", "enum", ("_________", 0)), 
		  ("foot_roll", "float", 0), 
		  ("heel_pivot", "float", 0), 
		  ("heel_slide", "float", 0), 
		  ("toe_pivot", "float", 0), 
		  ("toe_slide", "float", 0), 
		  ("ball_pivot", "float", 0), 
		  ("ball_slide", "float", 0),
		  ("banking", "float", 0)]


# spine joint chain
SPINEJNTCHAIN = ["sk_spine_root_jnt", "sk_spineA_jnt", "sk_spineB_jnt", "sk_spineC_jnt", "sk_chest_jnt"]
SPINECLSTRCHAIN = ["ikspine_clstr_1_clstr" ,"ikspine_clstr_2_clstr" ,
				   "ikspine_clstr_3_clstr" ,"ikspine_clstr_4_clstr" ,
				   "ikspine_clstr_5_clstr" ,"ikspine_clstr_6_clstr"]
IKSPINEHANDLE = "ikspine_ikhandle"
IKSPINECURVE = "ikspine_curve"
IKSPINECTRLCHAIN = ["ctrl_hips" ,"ctrl_fk_spine_A" ,"ctrl_midspine" ,"ctrl_fk_spine_B" ,"ctrl_chest"]

# head joint chain
HEADJNTCHAIN = ["sk_neck_base_jnt", "sk_neck_jnt", "sk_head_jnt"]
HEADCTRLCHAIN = ["ctrl_neck_base", "ctrl_neck", "ctrl_head"]






