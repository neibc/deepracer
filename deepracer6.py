# max angle : 13
# speed granularity : 3
# steering granularity : 3
# max speed : 3.8
# 4 hours training
# lane tracing

def reward_function(params):
    center_variance = params["distance_from_center"] / params["track_width"]
    
    left_lane = [5,6,7,8,9,10,11,12,13,14,81,82,83,84,85,86,87,88,89,90,91,92,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151]
    right_lane = [19,20,21,22,23,24,25,26,27,28,29,30,37,38,39,40,41,42,43,44,45,46,47,73,74,75,76,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133]
    center_lane = [0,1,2,3,4,5,15,16,17,18,19,31,32,33,34,35,36,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,77,78,79,80,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,134,135,152,153]
    
    reward = 21.0
    
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

    SPEED_THRESHOLD_1 = 1.3
    SPEED_THRESHOLD_2 = 2.5
	
    if params['speed'] < SPEED_THRESHOLD_1:
        reward *= 0.6
    elif params['speed'] <= SPEED_THRESHOLD_2:
        reward *= 0.8

    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 10

    # Penalize reward if the car is steering too much
    if abs(params['steering_angle']) > ABS_STEERING_THRESHOLD:  # Only need the absolute steering angle
        reward *= 0.8

    return reward
    
