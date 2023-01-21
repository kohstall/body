
import numpy as np
import time

# local stuff
import stembrain

# initialize body parts
spine = stembrain.Spine()


desired_position = np.array([0, 0, 0], dtype=np.int8)
force = np.array([0, 0, 0])
force_calibration = np.array([119, 120, 121])
#force_calibration = np.array([0, 0, 0])

# main superloop
while True:
    # --- heartbeat
    time.sleep(0.1)

    # --- calculations go here
    desired_position[0] = 50 * (1+np.cos(time.time()))
    desired_position[1] = 50 * (1+np.sin(time.time()))
    desired_position[2] = 30 #50 * (1+np.sin(0.5*time.time()))
    # desired_position[0] = 50 
    # desired_position[1] = 50 
    # desired_position[2] = 50 

    # --- Send motion commands to robot and receive sensor readings
    readings_raw = spine.communicate(np.concatenate([np.clip(desired_position,0,100), [-1]]))
    print(readings_raw)
    if isinstance(readings_raw, int):
        print('ERROR: no readings')
    else:
        # --- calculate force from readings
        force = (np.array(readings_raw[0:3])-force_calibration) * 1.0
        force[2] = -force[2] 
    
    # --- print readings
    print('desired position', desired_position, 'readings_raw', readings_raw, 'force', force)



    # === Experiments:
    # what are the best parameters, velocity, position, relative position, and how to integrate force
    # output language or python styled code?
    # output numbers or words like little far?
    # position or relative position


    # have a bench mark library of prompts


    # === promp examples
    # move to the left
    # touch the object
    # find the object
    # punch
    # clean up
    # make a happy motion
    # draw a triangle
    # make a zig zag
    # shift the object to the right

