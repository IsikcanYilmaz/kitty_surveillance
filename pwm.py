#!/usr/bin/python3

import RPi.GPIO as GPIO
import time, sys, os
import threading


class Motors():
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

        self.currentXval = 0
        self.currentYval = 0
        self.targetXval  = angleToPwm(45)
        self.targetYval  = angleToPwm(45)

        self.threadRunning = True
        self.pwmPollThread = threading.Thread(target=self.pwmPoll)
        self.pwmPollThread.start()

    def pwmPoll(self):
        while(self.threadRunning):
            if (self.currentXval != self.targetYval and abs(self.currentXval - self.targetXval) > PWM_INCREMENT_RATE):
                if (self.currentXval < self.targetXval):
                    self.currentXval += PWM_INCREMENT_RATE
                else:
                    self.currentXval -= PWM_INCREMENT_RATE
                print("[PWM] X %f->%f" % (self.currentXval, self.targetXval))
                self.pwmX.start(round(self.targetXval, SIG_FIGS))
            else:
                self.pwmX.stop()

            if (self.currentYval != self.targetXval and abs(self.currentYval - self.targetYval) > PWM_INCREMENT_RATE):
                if (self.currentYval < self.targetYval):
                    self.currentYval += PWM_INCREMENT_RATE
                else:
                    self.currentYval -= PWM_INCREMENT_RATE
                print("[PWM] Y %f->%f" % (self.currentYval, self.targetYval))
                self.pwmY.start(round(self.targetYval, SIG_FIGS))
            else:
                self.pwmY.stop()

            time.sleep(POLL_PERIOD)

    def setX(self, x):
        self.targetXval = angleToPwm(x)
        print("[PWM] Setting X to %d angles, pwm duty cycle to %f" % (x, self.targetXval))

    def setY(self, y):
        self.targetYval = angleToPwm(y)
        print("[PWM] Setting Y to %d angles, pwm duty cycle to %f" % (y, self.targetYval))

    def deinit(self):
        self.pwmX.stop()
        self.pwmY.stop()
        self.GPIO.cleanup()
        self.threadRunning = False


def angleToPwm(angle):
    return round((angle / 180.0) * 12.0, SIG_FIGS)

def main():
    if (len(sys.argv) != 4):
        print("USAGE: test_pwm.py <pwm> <duty_cycle> <seconds>")
        exit(1)
    pwm_choice = int(sys.argv[1])
    duty_cycle = float(sys.argv[2])
    seconds    = float(sys.argv[3])
    print("PWM %d at %f for %f seconds" % (pwm_choice, duty_cycle, seconds))



if __name__ == "__main__":
    pass
