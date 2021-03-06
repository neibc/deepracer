#from lee
#2019 lane
#max angle 25, angle granularity 3, max speed 3, speed granularity 3

def reward_function(params):

    center_variance = params["distance_from_center"]
    
    left_lane = [10,11,13,14,35,36,37,38,39,40,41,42,43,86,87,88,89,90,91,92,93,94,128,129,130,131,132,133,134,135,136,136,138,139,140,141,142,142,143]
    right_lane = [0,1,2,3,4,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,106,107,108,109,110,148,149,150,151,152,153]
    center_lane = [5,6,7,8,9,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,44,45,46,47,48,49,50,76,77,78,79,80,81,82,83,84,85,95,96,97,98,99,100,101,102,103,104,111,112,113,114,115,116,117,118,119,120,121,122,123,126,127,144,145,146,147]
    
    reward = 21
    
    if params["all_wheels_on_track"]:
        reward += 10
    else:
        reward -= 10
        
    if params["closest_waypoints"][1] in left_lane and params["is_left_of_center"]:
        reward += 10
    elif params["closest_waypoints"][1] in right_lane and not params["is_left_of_center"]:
        reward += 10
    elif params["closest_waypoints"][1] in center_lane and center_variance < 0.4:
        reward += 10
    else:
        reward -= 10

    SPEED_THRESHOLD_1 = 1.6
    SPEED_THRESHOLD_2 = 3.2
	
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
