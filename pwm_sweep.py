#!/usr/bin/python3

import RPi.GPIO as GPIO
import time, sys, os

PWM0_PIN = 12
PWM1_PIN = 13
NUMSWEEPS = 2
INCREMENT = 0.5
SLEEP    = 0.01
CEILING  = 10.0

if (len(sys.argv) != 2):
    exit(1)
pwm_choice = int(sys.argv[1])
print("PWM %d sweep" % (pwm_choice))

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

duty_cycle = 0.0
for i in range(0, NUMSWEEPS):
    while (duty_cycle <= CEILING):
        pwm.start(duty_cycle)
        time.sleep(SLEEP)
        duty_cycle += INCREMENT
        print(duty_cycle)

    while (duty_cycle > 0):
        pwm.start(duty_cycle)
        time.sleep(SLEEP)
        duty_cycle -= INCREMENT
        print(duty_cycle)

pwm.stop()
GPIO.cleanup()
