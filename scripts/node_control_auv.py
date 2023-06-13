#!/usr/bin/env python3

import time
import rospy
from std_msgs.msg import Int16, Bool, Float32
from pymavlink import mavutil
from PyMavlink import ROV

class Subscriber(object):
    def __init__(self, rov: ROV):
        self.rov = rov

        self.pwm_forward= 1500
        self.pwm_lateral = 1500

        # subscriber
        rospy.Subscriber('pwm_lateral', Int16, self.callback_pwm_lateral)
        rospy.Subscriber('pwm_forward', Int16, self.callback_pwm_forward)

    def callback_pwm_forward(self, data):
        self.pwm_forward = data.data
        print('Forward', data.data)
        self.rov.setRcValue(5, self.pwm_forward)

    def callback_pwm_lateral(self, data):
        self.pwm_lateral = data.data
        print('Lateral', data.data)
        self.rov.setRcValue(6, self.pwm_lateral)

    def spin(self):
        rospy.spin()

def main():
    master = mavutil.mavlink_connection('/dev/ttyACM2', baud=115200)
    # master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

    master.wait_heartbeat()

    rov = ROV(master)

    rov.arm()
    
    # rov.setMode('ALT_HOLD')

    rospy.init_node('node_control_auv', anonymous=True)

    subscriber = Subscriber(rov)

    subscriber.spin()

if __name__ == '__main__':
    main()