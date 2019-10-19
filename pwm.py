#!/usr/bin/python3

import RPi.GPIO as GPIO
import time, sys, os
import threading

PWM0_PIN = 12
PWM1_PIN = 13




class Pwms():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PWM0_PIN, GPIO.OUT)
        GPIO.setup(PWM1_PIN, GPIO.OUT)
        self.pwmX = GPIO.PWM(PWM0_PIN, 50)
        self.pwmY = GPIO.PWM(PWM1_PIN, 50)
        self.lastXpos = 45
        self.lastYpos = 45
        self.pwmXval = self.lastXpos
        self.pwmYval = self.lastYpos

    def pwmStopTimerThread(self, t, pwm):
        time.sleep(t)
        print("[PWM] Stopping pwm", pwm);
        pwm.stop()

    def setX(self, x):
        self.pwmXval = angleToPwm(x)
        self.pwmX.start(self.pwmXval)
        print("[PWM] Setting X to %d angles, pwm duty cycle to %f" % (x, self.pwmXval))
        timer = threading.Thread(target=self.pwmStopTimerThread, args=(1, self.pwmX))
        self.lastXpos = x
        timer.start()

    def setY(self, y):
        self.pwmYval = angleToPwm(y)
        self.pwmY.start(angleToPwm(y))
        print("[PWM] Setting Y to %d angles, pwm duty cycle to %f" % (y, self.pwmYval))
        timer = threading.Thread(target=self.pwmStopTimerThread, args=(1, self.pwmY))
        self.lastYpos = y
        timer.start()

    def deinit(self):
        pwmX.stop()
        pwmY.stop()
        GPIO.cleanup()


def angleToPwm(angle):
    return (angle / 180.0) * 12.0

def main():
    if (len(sys.argv) != 4):
        print("USAGE: test_pwm.py <pwm> <duty_cycle> <seconds>")
        exit(1)
    pwm_choice = int(sys.argv[1])
    duty_cycle = float(sys.argv[2])
    seconds    = float(sys.argv[3])
    print("PWM %d at %f for %f seconds" % (pwm_choice, duty_cycle, seconds))

    #p = Pwms()

   
if __name__ == "__main__":
    p = Pwms()
    x = y = 45
    while True:
        p.setX(x)
        p.setY(y)
        x = int(input("ENTER X"))
        y = int(input("ENTER Y"))
