
import numpy as np
import time

# local stuff
import stembrain

FORCE_THRESHOLD = 10


class Cerebellum():

    def __init__(self):
        self.spine = stembrain.Spine()
        self.desired_position = np.array([0, 0, 0], dtype=np.int8)
        self.force = np.array([0, 0, 0])
        self.force_calibration = np.array([119, 120, 121])
        #command_list = ["waypoint_motion([-2, 2], 1, "continue")","waypoint_motion([2, 0], 1, "continue")","waypoint_motion([-2, -2], 1, "continue")"]
        #force_calibration = np.array([0, 0, 0])

        self.t0 = time.time()
        # main superloop
        self.start_waypoint = np.array([0, 0])
        self.start_time = time.time()

    def move(self, target_waypoint, velocity, mode):

        while True:
        # --- heartbeat
            time.sleep(0.1)

            t = time.time() - self.t0
            t_current_move = time.time() - self.start_time

            # --- calculations go here
            target_waypoint = np.array([0, 1])
            velocity = 1
            distance = np.linalg.norm(target_waypoint - self.start_waypoint)
            ramp_progress = t_current_move / distance * velocity

            self.current_position[0:2] = 10 * (self.start_waypoint + (target_waypoint - self.start_waypoint) * ramp_progress)
            self.current_position[2] = 30 

            # --- Send motion commands to robot and receive sensor readings
            readings_raw = self.spine.communicate(np.concatenate([np.clip(self.current_position,0,100), [-1]]))
            print(readings_raw)
            if isinstance(readings_raw, int):
                print('ERROR: no readings')
            else:
                # --- calculate force from readings
                self.force = (np.array(readings_raw[0:3])-self.force_calibration) * 1.0
                self.force[2] = -self.force[2] 
            
            # --- print readings
            print('desired position', self.current_position, 'readings_raw', readings_raw, 'force', self.force)

            if ramp_progress >= 1:
                return self.current_position[0:2], 0

            if mode =='stop' and any(self.force > FORCE_THRESHOLD):
                return self.current_position[0:2], 1















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

