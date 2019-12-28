#!/usr/bin/python3

import RPi.GPIO as GPIO
from pwm_sweep import *
import time, sys, os
import threading

from common import *

MOTOR_PWM_FREQUENCY = 50 # Hz

PWM0_INDEX = 0 # X
PWM1_INDEX = 1 # Y


# TODO # there's a lot of redundancy, and frankly ugly looking code. this is mostly due to not understanding
# how the pointer equivalent in python works. TODO refactor

# TODO PLEASE FOR THE LOVE OF GOD CLEAN UP THIS CODE


class Motors():
    def __init__(self):
        # Initialize PWM channels for servos
        self.pwmX = self.pwmInit(PWM0_PIN)
        self.pwmY = self.pwmInit(PWM1_PIN)
        self.pwmObjects = [self.pwmX, self.pwmY]

        self.lastXpos = 45
        self.lastYpos = 45
        self.pwmXval = self.lastXpos
        self.pwmYval = self.lastYpos

        self.targetXval = angleToPwm(45)
        self.targetYval = angleToPwm(45)
        self.targets    = [self.targetXval, self.targetYval]

        self.xChanged = False
        self.yChanged = False
        self.xChangedEvent = threading.Event()
        self.yChangedEvent = threading.Event()
        self.threadChangedEvents = [self.xChangedEvent, self.yChangedEvent]

        self.threadXRunning = False
        self.threadYRunning = False
        self.threadXRunningLock = threading.Lock()
        self.threadYRunningLock = threading.Lock()

        self.threadRunningFlags = [self.threadXRunning, self.threadYRunning]
        self.threadXInstance = threading.Thread(target=self.pollThreadFn, args=[self.pwmX, self.threadRunningFlags, self.threadChangedEvents, self.targets, PWM0_PIN])
        #self.threadYInstance = threading.Thread(target=self.threadY, args=[self.pwmY, self.yChanged, self.threadYRunning, PWM1_PIN])

        #self.threadRunning = True
        #self.pwmPollThread = threading.Thread(target=self.pwmPoll)
        #self.pwmPollThread.start()

        self.threadXInstance.start()

    def pwmInit(self, pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        pwm = GPIO.PWM(pin, MOTOR_PWM_FREQUENCY)
        pwm.start(0)
        return pwm

    def setAngle(self, pwm, pin, angle):
        duty = angleToPwm(angle)
        print("[PWM] SET ANGLE pin %d to %d (%f)" % (pin, angle, duty))
        GPIO.output(pin, True)
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.25) # TODO VARIABLE SLEEP TIME
        GPIO.output(pin, False)
        pwm.ChangeDutyCycle(0)

    # The thread function that drives one servo motor.
    def pollThreadFn(self, pwm, runningFlags, valChangedEvents, targets, pin):
        # BENDING OVER BACKWARDS DUE TO BEING UNABLE TO PASS A POINTER TO THIS THREAD
        print(runningFlags)
        if (pin == PWM0_PIN): # THIS MOTOR IS THE X AXIS ONE
            motor_str = "X"
            pin_index = PWM0_INDEX
        elif (pin == PWM1_PIN):
            motor_str = "Y"
            pin_index = PWM1_INDEX
        else:
            print("[PWM !] INCORRECT PIN.")
            return
        print("[PWM] Thread for motor %s created." % (motor_str))
        runningFlags[pin_index] = True
        while runningFlags[pin_index]:
            valChangedEvents[pin_index].wait()
            print("[PWM] Setting %s to %d degrees" % (motor_str, targets[pin_index]), targets, runningFlags)
            self.setAngle(self.pwmObjects[pin_index], pin, targets[pin_index])
            valChangedEvents[pin_index].clear()
        print("[PWM] Thread %s exiting." % (motor_str))

    def setX(self, x):
        self.targetXval = angleToPwm(x)
        self.targets[PWM0_INDEX] = x
        self.xChanged = True
        self.xChangedEvent.set()
        #print("[PWM] Setting X to %d angles, pwm duty cycle to %f" % (x, self.targetXval))

    def setY(self, y):
        self.targetYval = angleToPwm(y)
        self.yChanged = True
        #print("[PWM] Setting Y to %d angles, pwm duty cycle to %f" % (y, self.targetYval))

    def deinit(self):
        self.pwmX.stop()
        self.pwmY.stop()
        self.GPIO.cleanup()
        self.threadRunning = False
        self.threadXInstance.join()


def angleToPwm(angle):
    return (angle/18) + 2

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
