aimbot

ROS node for aiming turret given location of enemy robot.

	Published Topics
		/aimbot/output_pose (geometry_msgs/PoseStamped)
			Calculated pose to send to turret to aim at detected robot.

	Subscribed Topics
		/aimbot/detected_enemy (aimbot_msgs/DetectedRobot)
			Detected bearing and distance of the enemy robot relative to the turret frame, in radians. Since turret frame is (x forward, y right, z down), the y_rotation is (+up, -down) and z_rotation is (+right, -left).

	Services

	Messages
		aimbot_msgs/DetectedRobot.msg
			# The position and bearing of the detected robot in radians.
			float64 distance
			float64 y_rotation
			float64 z_rotation