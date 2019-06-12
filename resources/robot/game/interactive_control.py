import sys
sys.path.append("../project_files/robot_drivers/")

import Adafruit_PCA9685
import time
from hex_walker_driver import *


# Declare globals
global right_side
global left_side
global hex_walker

def setup():
    #init the pwm stuffs and run selected tests
    global right_side
    global left_side
    global hex_walker

    right_side = Adafruit_PCA9685.PCA9685(address=0x40)
    left_side = Adafruit_PCA9685.PCA9685(address=0x41)
    # create some legs
    right_side.set_pwm_freq(60)
    left_side.set_pwm_freq(60)
    rf = Leg(0, right_side, 0, 1, 2, 0)
    rm = Leg(1, right_side, 3, 4, 5, 1)
    rr = Leg(2, right_side, 6, 7, 8, 2)
    lr = Leg(3, left_side, 0, 1, 2, 3)
    lm = Leg(4, left_side, 6, 4, 5, 4)
    lf = Leg(5, left_side, 3, 7, 8, 5)
    right_legs = [rf, rm, rr]
    left_legs = [lr, lm, lf]

    # Setup robot
    hex_walker = Hex_Walker(rf, rm, rr, lr, lm, lf)
    hex_walker.do_move_set([TALL_NEUTRAL])


def command_arbiter(dist, command):
    global hex_walker

    if command == 'w':
        hex_walker.walk(dist, 0)
    elif command == 'a':
        tall_side_walk_test(hex_walker, 'left')
    elif command == 's':
        hex_walker.walk(dist, 180)
    elif command == 'd':
        tall_side_walk_test(hex_walker, 'right')
    elif command == 'q':
        tall_rotate_test(hex_walker, 'left')
    elif command == 'e':
        tall_rotate_test(hex_walker, 'right')
    elif command == 'wd':
        hex_walker.walk(dist, 60)
    elif command == 'wa':
        hex_walker.walk(dist, 300)
    elif command == 'sd':
        hex_walker.walk(dist, 120)
    elif command == 'sa':
        hex_walker.walk(dist, 240)
    elif command == 'qq':
        tall_fine_rotate_test(hex_walker, 'left')
    elif command == 'ee':
        tall_fine_rotate_test(hex_walker, 'right')
    elif command == 'z':
        hex_walker.bounce(0.1, 10)
        


def tall_side_walk_test(hw, direction):
    hw.speed = 0.1
    moves = [
    TALL_NEUTRAL,
    TALL_TRI_FRONT_CENTER_UP_OUT_BACK_NEUTRAL,
    TALL_TRI_FRONT_CENTER_OUT_BACK_UP_NEUTRAL,
    TALL_TRI_FRONT_BACKWARDS_BACK_UP_NEUTRAL,
    TALL_TRI_FRONT_BACKWARDS_BACK_NEUTRAL,
    TALL_TRI_FRONT_UP_NEUTRAL_BACK_NEUTRAL,
    TALL_TRI_FRONT_UP_NEUTRAL_BACK_BACKWARDS,
    TALL_TRI_FRONT_NEUTRAL_BACK_BACKWARDS,
    TALL_TRI_FRONT_NEUTRAL_BACK_UP_NEUTRAL,
    ]

    if direction == 'left':
        hw.set_new_front("3-4")
    else: 
        hw.set_new_front("0-1")

    hw.do_move_set(moves)
    hw.set_new_front("5-0")
    hw.do_move_set([TALL_NEUTRAL])


def walk(hw, direction):
    if direction == 'forward':
        hw.walk(1,0)
    elif direction == 'backward':
        hw.walk(1,180)
    elif direction == 'right_forward':
        hw.walk(1,60)
    elif direction == 'left_forward':
        hw.walk(1,300)
    elif direction == 'right_backward':
        hw.walk(1,120)
    elif direction == 'left_backward':
        hw.walk(1,240)

    hw.do_move_set([TALL_NEUTRAL])


def tall_rotate_test(hw, direction):
    if direction == 'left':
        hex_walker.rotate(1, LEFT)
    else:
        hex_walker.rotate(1, RIGHT)

    hw.do_move_set([TALL_NEUTRAL])


def tall_fine_rotate_test(hw, direction):
    if direction == 'left':
        hex_walker.fine_rotate(1, LEFT)
    else:
        hex_walker.fine_rotate(1, RIGHT)

    hw.do_move_set([TALL_NEUTRAL])

def leg_ripple(hw, direction):
    if direction == 'left':
        hex_walker.leg_wave(LEFT, .1, 4)
    else:
        hex_walker.leg_wave(RIGHT, .1, 4)

    hw.do_move_set([TALL_NEUTRAL])
