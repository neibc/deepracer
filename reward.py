def reward_function(params):
	'''
	modified from amazon deepracer sample codes. maximum speed 5m/s, speed granularity 2, steering angle granularity 5(or 7)
	2019, May 8, deepracer preview console
	'''

	# Calculate 3 marks that are farther and father away from the center line
	marker_1 = 0.3 * params['track_width']
	marker_2 = 0.4 * params['track_width']
	marker_3 = 0.5 * params['track_width']

	# Give higher reward if the car is closer to center line and vice versa
	if params['distance_from_center'] <= marker_1:
		reward = 1
	elif params['distance_from_center'] <= marker_2:
		reward = 0.8
	elif params['distance_from_center'] <= marker_3:
		reward = 0.7
	else:
		reward = 1e-3  # likely crashed/ close to off track

	# penalize reward for the car taking slow actions
	# speed is in m/s
	# the below assumes your action space has a maximum speed of 5 m/s and speed granularity of 3
	# we penalize any speed less than 2m/s
	SPEED_THRESHOLD_1 = 2
	SPEED_THRESHOLD_2 = 4
	if params['speed'] < SPEED_THRESHOLD_1:
		reward *= 0.1
	elif params['speed'] <= SPEED_THRESHOLD_2:
		reward *= 0.3

	# Steering penality threshold, change the number based on your action space setting
	ABS_STEERING_THRESHOLD = 15

	# Penalize reward if the car is steering too much
	if abs(params['steering_angle']) > ABS_STEERING_THRESHOLD:  # Only need the absolute steering angle
		reward *= 0.5
	return float(reward)
