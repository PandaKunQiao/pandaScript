# for arm controls
ARMJNTCHAIN = ["sk_l_shoulder_jnt", "sk_l_elbow_jnt", "sk_l_wrist_jnt"]
IKARMJNTCHAIN = ["ik_l_shoulder_jnt" ,"ik_l_elbow_jnt" ,"ik_l_wrist_jnt"]
FKARMJNTCHAIN = ["fk_l_shoulder_jnt" ,"fk_l_elbow_jnt" ,"fk_l_wrist_jnt"]
IKARMCTRLCHAIN = ["ctrl_l_ik_elbow" ,"ctrl_l_ik_wrist"]
FKARMCTRLCHAIN = ["ctrl_l_fk_shoulder" ,"ctrl_l_fk_elbow" ,"ctrl_l_fk_wrist"]


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





# for foot controls
LEGJNTCHAIN = ["sk_l_femur_jnt" ,"sk_l_knee_jnt" ,"sk_l_ankle_jnt" ,"sk_l_ball_jnt" ,"sk_l_toe_jnt"]
IKLEGJNTCHAIN = ["ik_l_femur_jnt" ,"ik_l_knee_jnt" ,"ik_l_ankle_jnt"]
FKLEGJNTCHAIN = ["fk_l_femur_jnt" ,"fk_l_knee_jnt" ,"fk_l_ankle_jnt"]

LEGFKCTRLCHAIN = ["ctrl_l_fk_femur" ,"ctrl_l_fk_knee" ,"ctrl_l_fk_ankle"]
LEGIKCTRLCHAIN = ["ctrl_l_knee" ,"ctrl_l_ik_foot"]

REVERSEFOOTJNTCHAIN = ["rf_l_outFoot_jnt", "rf_l_inFoot_jnt", "rf_l_heel_jnt", "rf_l_toe_jnt", "rf_l_ball_jnt", "rf_l_ankle_jnt"]
REVERSEFOOTIKHANDLECHAIN = ["ikleg_l_ankle_ikhandle" ,"rf_l_ball_ikhandle" ,"rf_l_toe_ikhandle"]

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





