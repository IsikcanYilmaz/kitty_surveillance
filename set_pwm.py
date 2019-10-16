#!/usr/bin/python3

import RPi.GPIO as GPIO
import time, sys, os

PWM0_PIN = 12
PWM1_PIN = 13

if (len(sys.argv) != 4):
    print("USAGE: test_pwm.py <pwm> <duty_cycle> <seconds>")
    exit(1)
pwm_choice = int(sys.argv[1])
duty_cycle = float(sys.argv[2])
seconds    = float(sys.argv[3])
print("PWM %d at %f for %f seconds" % (pwm_choice, duty_cycle, seconds))

GPIO.setmode(GPIO.BCM)

if (pwm_choice == 0):
    GPIO.setup(PWM0_PIN, GPIO.OUT)
    pwm = GPIO.PWM(PWM0_PIN, 50)
elif (pwm_choice == 1):
    GPIO.setup(PWM1_PIN, GPIO.OUT)
    pwm = GPIO.PWM(PWM1_PIN, 50)
else:
    GPIO.cleanup()
    exit(1)

pwm.start(duty_cycle)
time.sleep(seconds)
pwm.stop()
GPIO.cleanup()
