#!/usr/bin/env python

import sys
sys.path.append("/home/pi/Lynxmotion_Hexapod/project_files/robot_drivers/")

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from time import sleep
import Adafruit_PCA9685
from hex_walker_driver import *

#init the pwm stuffs and run selected tests
pwm_40= Adafruit_PCA9685.PCA9685(address=0x40)
pwm_41= Adafruit_PCA9685.PCA9685(address=0x41)

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

global finish_hex_pub
global finish_torso_pub
global torso_done
global hex_done
torso_done = 0
hex_done = 0

def do_hex_walker_command(data):
    global hex_done
    global finish_hex_pub
    rospy.loginfo(rospy.get_caller_id() + ' I heard %s', data.data)
    if not data.data:
        print("Not doing anything since I heard nothing.")
        pass
    else:
        commandlist = data.data.split()
        if commandlist[0] == "walk":
            if len(commandlist) != 3:
                assert "incorrect number of arguments for walk"
            num_steps = int(commandlist[1])
            direction = int(commandlist[2])
            print("walking " + str(num_steps) + " steps forward in direction " + str(direction))
            hex_walker.walk(num_steps, direction)
        elif commandlist[0] == "rotate":
            if len(commandlist) != 3:
                assert "incorrect number of arguments for rotate"
            num_steps = int(commandlist[1])
            if(commandlist[2] == "left"):
                direction = LEFT
            else:
                direction = RIGHT
            print("rotating " + str(num_steps) + commandlist[2])
            hex_walker.rotate(num_steps, direction)
        elif commandlist[0] == "leg_wave":
            if len(commandlist) != 3:
                assert "incorrect number of arguments for leg_wave"
            num_times = int(commandlist[1])
            if(commandlist[2] == "left"):
                direction = LEFT
            else:
                direction = RIGHT
            print("leg waving " + str(num_times) + " in the direction " + commandlist[2])
            hex_walker.leg_wave(direction, .1, num_times)
        elif commandlist[0] == "bounce":
            if len(commandlist) != 3:
                assert "incorrect number of arguments for bounce"
            num_times = int(commandlist[1])
            wait_time = float(commandlist[2])
            print("bouncing " + str(num_times) + " for " + str(wait_time) + " seconds.")
            hex_walker.bounce(wait_time, num_times)
        else:
            print("MOTION: Received a non-empty and non-supported motion. Tied to match \"{}\" to no avail.".format(commandlist[0]))


    hex_done = hex_done + 1
    finish_hex_pub.publish(hex_done)    

def do_torso_command(data):
    global torso_done
    global finish_torso_pub
    rospy.loginfo(rospy.get_caller_id() + ' I heard %s', data.data)
    if not data.data:
        print("Not doing anything since I heard nothing.")
        pass
    else:
        commandlist = data.data.split()
        
        if commandlist[0] == "wave":
            if len(commandlist) != 3:
                assert "incorrect number of arguments for wave"
            num_times = int(commandlist[1])
            direction = int(commandlist[2])
            print("waving " + str(num_times) + " times in direction " + str(direction))
            torso.wave(direction, num_times)
        elif commandlist[0] == "king_kong":
            if len(commandlist) != 3:
                assert "incorrect number of arguments for king_kong"
            num_times = int(commandlist[1])
            direction = int(commandlist[2])
            print("king_kong-ing " + str(num_times) + " times in direction " + str(direction))
            torso.king_kong(direction, num_times)
        elif commandlist[0] == "monkey":
            if len(commandlist) != 2:
                assert "incorrect number of arguments for monkey"
            num_times = int(commandlist[1])
            print("monkeying " + str(num_times) + " times")
            torso.monkey(num_times)
        elif commandlist[0] == "handshake":
            if len(commandlist) != 3:
                assert "incorrect number of arguments for handshake"
            num_times = int(commandlist[1])
            direction = int(commandlist[2])
            torso.hand_shake(direction, num_times) 
        elif commandlist[0] == "point":
            if len(commandlist) != 3:
                assert "incorrect number of arguments for pointing"
            if commandlist[1] == "right":
                direction = RIGHT
            else:
                direction = LEFT
            wait_time = float(commandlist[2])
            torso.point(direction, wait_time)
        elif commandlist[0] == "look":
            if len(commandlist) != 1:
                assert "incorrect number of arguments for looking"
            torso.look()
        elif commandlist[0] == "neutral":
            if len(commandlist) != 2:
                assert "incorrect number of arguments for returning to neutral"
            direction = int(commandlist[1])
            torso.neutral_rotate(direction)
        elif commandlist[0] == "turn":
            if len(commandlist) != 2:
                assert "incorrect number of arguments for looking"
            direction = int(commandlist[1])
            torso.set_torso_rotation(direction)
        else:
            print("TORSO: Received a non-empty and non-supported motion. Tied to match \"{}\" to no avail.".format(commandlist[0]))
    
    # make sure we don't set done too fast. probably unnecessary but it is safer
    sleep(.1)
    torso_done = torso_done + 1
    finish_torso_pub.publish(torso_done)    


def node_setup():
    global finish_hex_pub
    global finish_torso_pub
    rospy.init_node('hexapod_motion_controller')
    rospy.Subscriber('motion_command', String, do_hex_walker_command)
    rospy.Subscriber('torso_command', String, do_torso_command)
    finish_hex_pub = rospy.Publisher('motion_command_finished', Int32, queue_size = 1) 
    finish_torso_pub = rospy.Publisher('torso_command_finished', Int32, queue_size = 1)
    finish_hex_pub.publish(0)
    finish_torso_pub.publish(0)
    

    rf_tip = rospy.Publisher('legs/rf_tip', Int32, queue_size=1)
    rf_mid = rospy.Publisher('legs/rf_mid', Int32, queue_size=1)
    rf_rot = rospy.Publisher('legs/rf_rot', Int32, queue_size=1)
    
    rm_tip = rospy.Publisher('legs/rm_tip', Int32, queue_size=1)
    rm_mid = rospy.Publisher('legs/rm_mid', Int32, queue_size=1)
    rm_rot = rospy.Publisher('legs/rm_rot', Int32, queue_size=1)
    
    rr_tip = rospy.Publisher('legs/rr_tip', Int32, queue_size=1)
    rr_mid = rospy.Publisher('legs/rr_mid', Int32, queue_size=1)
    rr_rot = rospy.Publisher('legs/rr_rot', Int32, queue_size=1)
    
    lf_tip = rospy.Publisher('legs/lf_tip', Int32, queue_size=1)
    lf_mid = rospy.Publisher('legs/lf_mid', Int32, queue_size=1)
    lf_rot = rospy.Publisher('legs/lf_rot', Int32, queue_size=1)
    
    lm_tip = rospy.Publisher('legs/lm_tip', Int32, queue_size=1)
    lm_mid = rospy.Publisher('legs/lm_mid', Int32, queue_size=1)
    lm_rot = rospy.Publisher('legs/lm_rot', Int32, queue_size=1)
    
    lr_tip = rospy.Publisher('legs/lr_tip', Int32, queue_size=1)
    lr_mid = rospy.Publisher('legs/lr_mid', Int32, queue_size=1)
    lr_rot = rospy.Publisher('legs/lr_rot', Int32, queue_size=1)
    
    want_publish = True
    
    # robot data publication
    if want_publish:
        refresh_rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            rf_tip.publish(hex_walker.leg0.tip_motor_angle)
            rf_mid.publish(hex_walker.leg0.mid_motor_angle)
            rf_rot.publish(hex_walker.leg0.rot_motor_angle)
            
            rm_tip.publish(hex_walker.leg1.tip_motor_angle)
            rm_mid.publish(hex_walker.leg1.mid_motor_angle)
            rm_rot.publish(hex_walker.leg1.rot_motor_angle)

            rr_tip.publish(hex_walker.leg2.tip_motor_angle)
            rr_mid.publish(hex_walker.leg2.mid_motor_angle)
            rr_rot.publish(hex_walker.leg2.rot_motor_angle)

            lf_tip.publish(hex_walker.leg3.tip_motor_angle)
            lf_mid.publish(hex_walker.leg3.mid_motor_angle)
            lf_rot.publish(hex_walker.leg3.rot_motor_angle)

            lm_tip.publish(hex_walker.leg4.tip_motor_angle)
            lm_mid.publish(hex_walker.leg4.mid_motor_angle)
            lm_rot.publish(hex_walker.leg4.rot_motor_angle)

            lr_tip.publish(hex_walker.leg5.tip_motor_angle)
            lr_mid.publish(hex_walker.leg5.mid_motor_angle)
            lr_rot.publish(hex_walker.leg5.rot_motor_angle)
    
            refresh_rate.sleep()
    else:
        rospy.spin()

if __name__ == '__main__':
    node_setup()
