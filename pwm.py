#!/usr/bin/python3

import RPi.GPIO as GPIO
import pigpio
import time, sys, os

from common import *

MOTOR_PWM_FREQUENCY = 50 # Hz

class Motors():
    def __init__(self):
        # Initialize PWM channels for servos
        self.pigpioInstance = pigpio.pi()
        self.pigpioInstance.set_mode(PWM0_PIN, pigpio.OUTPUT)
        self.pigpioInstance.set_mode(PWM1_PIN, pigpio.OUTPUT)

    def setX(self, x):
        self.pigpioInstance.set_servo_pulsewidth(X_AXIS_PIN, angleToPwm(x) + 500)
        time.sleep(PWM_SLEEP_DURATION)

    def setY(self, y):
        self.pigpioInstance.set_servo_pulsewidth(Y_AXIS_PIN, angleToPwm(y) + 500)
        time.sleep(PWM_SLEEP_DURATION)

    def deinit(self):
        self.pwmX.stop()
        self.pwmY.stop()
        self.GPIO.cleanup()
        self.threadRunning = False
        self.threadXInstance.join()


def angleToPwm(angle):
    return 2000 * angle / 180

def main():
    motors = Motors()
    while True:
        a = input("[*] Enter Angle:")
        a_int = int(a)
        motors.setX(a_int)
        #print(motors.targets)
        #motors.threadRunningFlags[PWM0_INDEX] = False
    print("break out")
    while True:
        pass

if __name__ == "__main__":
    main()
