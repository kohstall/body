
import serial
import numpy as np
import time

class Spine():

    def __init__(self, port='/dev/tty.usbmodem33028801', baud_rate=1000000):
        try:
            self.ser = serial.Serial(port, baud_rate)
        except:
            print('ERROR: Spine could not be connected')

    def communicate(self, commands):
        
        commands_package = bytes(commands.astype(dtype=np.int8))
        #print('writing', commands_package, 'to spine')
        self.ser.write(commands_package)

        # --- Receive readings
        #print('bytes available',self.ser.in_waiting)
        if self.ser.in_waiting:

            readings_bytes = self.ser.read(8)

            # --- CHECK for more stuff in buffer and empty it
            while self.ser.in_waiting:
                self.ser.read()
                print("[readings] ERROR: extrabytes")

            # --- DECODE readings

            readings_raw = np.frombuffer(readings_bytes, dtype=np.uint8)
            return readings_raw
        else:
            return -1

if __name__=="__main__":
    spine = Spine()
    commands = np.array([0, 00, 0, 8], dtype=np.int16)
    while True:
        readings = spine.communicate(commands)
        print('main readings', readings)
        time.sleep(0.3)
