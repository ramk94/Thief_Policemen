import sys

sys.path.append("../robot_drivers/")
import zerorpc
import Adafruit_PCA9685
import time
from hex_walker_driver import *

# init the pwm stuffs and run selected tests
pwm_40 = Adafruit_PCA9685.PCA9685(address=0x40)
pwm_41 = Adafruit_PCA9685.PCA9685(address=0x41)

pwm_40.set_pwm_freq(60)
pwm_41.set_pwm_freq(60)

# create somee legs
rf = Leg(0, pwm_40, 0, 1, 2, 0)
rm = Leg(0, pwm_40, 3, 4, 5, 1)
rr = Leg(0, pwm_40, 6, 7, 8, 2)
lr = Leg(0, pwm_41, 0, 1, 2, 3)
lm = Leg(0, pwm_41, 6, 4, 5, 4)
lf = Leg(0, pwm_41, 3, 7, 8, 5)

# create the hex walker
hex_walker = Hex_Walker(rf, rm, rr, lr, lm, lf)

# create the torso
r = Leg(0, pwm_41, 12, 11, 10, ARM_R)
l = Leg(0, pwm_40, 12, 11, 10, ARM_L)
rot = Rotator(0, pwm_40, 9)

torso = Robot_Torso(r, l, rot)

import zerorpc


class Thief(object):
    def rotate(self, alpha):
        alpha = alpha % 360
        if alpha > 180:
            alpha -= 360
        beta = 30.0
        if alpha > 0:
            seconds = alpha / beta
            hex_walker.rotate(int(seconds), RIGHT)
        else:
            seconds = -alpha / beta
            hex_walker.rotate(int(seconds), LEFT)
        print('rotate {}'.format(alpha))

    def move_forward(self, n):
        seconds = n * 2
        hex_walker.walk(int(seconds), 0)
        print('move {}'.format(n))

    def get_sensor_data(self):
        data = None
        return data


try:
    s = zerorpc.Server(Thief())
    s.bind("tcp://0.0.0.0:4242")
    s.run()
except:
    pass
