
import numpy as np
import time

# local stuff
import stembrain

# initialize body parts
spine = stembrain.Spine()


desired_position = np.array([0, 0, 0], dtype=np.int16)
force = np.array([0, 0, 0])
farce_calibration = np.array([109, 110, 111])

# main superloop
while True:
    # --- heartbeat
    time.sleep(0.1)

    # --- calculations go here
    desired_position[0] = 50 * (1+np.cos(time.time()))
    desired_position[1] = 50 * (1+np.sin(0.5*time.time()))
    desired_position[2] = 50 * (1+np.sin(0.5*time.time()))

    # --- Send motion commands to robot and receive sensor readings
    readings_raw = spine.communicate(np.concatenate([np.clip(desired_position,0,100), [-1]]))
    print(readings_raw)
    if isinstance(readings_raw, int):
        print('ERROR: no readings')
    else:
        # --- calculate force from readings
        force = (np.array(readings_raw[0:3])-farce_calibration) * 1.0
        force[2] = -force[2] 
    
    # --- print readings
    print('desired position', desired_position, 'readings_raw', readings_raw, 'force', force)