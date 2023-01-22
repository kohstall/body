import numpy as np
import time

# local stuff
import stembrain

FORCE_THRESHOLD = 5


class Cerebellum:
    def __init__(self):
        self.spine = stembrain.Spine()
        self.current_position = np.array([0, 0, 0], dtype=np.int8)
        self.force = np.array([0, 0, 0])
        self.force_calibration = np.array([152, 120, 119])
        # command_list = ["position_motion([-2, 2], 1, "continue")","position_motion([2, 0], 1, "continue")","position_motion([-2, -2], 1, "continue")"]
        # force_calibration = np.array([0, 0, 0])

        self.t0 = time.time()
        # main superloop
        self.current_position = np.array([0, 0])
        self.touch_detected = 0

        position_command = np.zeros(3)
        position_command[2] = 30
        readings_raw = self.spine.communicate(
            np.concatenate([np.clip(position_command, 0, 100), [-1]])
        )

    def move(self, target_position, velocity, mode):
        start_position = self.current_position
        start_time = time.time()
        distance = np.linalg.norm(target_position - start_position)
        T = distance / velocity
        self.touch_detected = 0
        i = 0
        while True and T > 0:
            # --- heartbeat
            time.sleep(0.02)

            # --- calculations go here
            ramp_progress = (time.time() - start_time) / T

            self.current_position = (
                start_position + (target_position - start_position) * ramp_progress
            )

            # --- Send motion commands to robot and receive sensor readings
            position_command = np.zeros(3)
            position_command[0:2] = 50 + 10 * self.current_position
            position_command[2] = 30

            readings_raw = self.spine.communicate(
                np.concatenate([np.clip(position_command, 0, 100), [-1]])
            )
            # print(readings_raw)
            if isinstance(readings_raw, int):
                print("ERROR: no readings")
            else:
                # --- calculate force from readings
                self.force = (
                    np.array(readings_raw[0:3]) - self.force_calibration
                ) * 1.0
                self.force[2] = -self.force[2]

            # --- print readings
            i += 1
            if i % 1000 == 0:
                print(
                    "current_position",
                    self.current_position,
                    "readings_raw",
                    readings_raw,
                    "force",
                    self.force,
                    "ramp_progress",
                    ramp_progress,
                )

            if ramp_progress >= 1:
                print("cerebellum done without touch")
                break

            if mode == "stop" and any(np.abs(np.array(self.force)) > FORCE_THRESHOLD):
                print("cerebellum done with touch")
                self.touch_detected = 1
                break

        if any(np.abs(np.array(self.force)) > FORCE_THRESHOLD):
            self.touch_detected = 1
        return self.current_position, self.touch_detected, mode

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
