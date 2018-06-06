

# for hand controls
FINGERCTRLCHAIN = ["ctrl_l_thumb_A", "ctrl_l_thumb_B", "ctrl_l_thumb_C", 
					"ctrl_l_index_A", "ctrl_l_index_B", "ctrl_l_index_C", 
					"ctrl_l_middle_A", "ctrl_l_middle_B", "ctrl_l_middle_C", 
					"ctrl_l_ring_A", "ctrl_l_ring_B", "ctrl_l_ring_C", 
					"ctrl_l_little_A", "ctrl_l_little_B", "ctrl_l_little_C"]

FINGERATTRLS = [("custom_attributes", "enum", ("_________", 0)),
				("fist", "float", 0),
				("neutral"， "float", 0),
				("claw", "float", 0),
				("bind", "float", 0)]


# for foot controls
REVERSEFOOTJNTCHAIN = ["rf_l_outFoot_jnt", "rf_l_inFoot_jnt", "rf_l_heel_jnt", "rf_l_toe_jnt", "rf_l_ball_jnt", "rf_l_ankle_jnt"]

RFATTRLS = [("custom_attributes", "enum", ("_________", 0)), 
		  ("foot_roll", "float", 0), 
		  ("heel_pivot", "float", 0), 
		  ("heel_slide", "float", 0), 
		  ("toe_pivot", "float", 0), 
		  ("toe_slide", "float", 0), 
		  ("ball_pivot", "float", 0), 
		  ("ball_slide", "float", 0),
		  ("banking", "float", 0)]