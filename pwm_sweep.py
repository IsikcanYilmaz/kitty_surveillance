#!/usr/bin/python3

import RPi.GPIO as GPIO
import time, sys, os, random

PWM0_PIN = 12
PWM1_PIN = 13
NUMSWEEPS = 2
INCREMENT = 0.5
SLEEP    = 0.06
CEILING  = 12.0

def sweep():
    #if (len(sys.argv) != 2):
    #    exit(1)
    #pwm_choice = int(sys.argv[1])
    pwm_choice = 1
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
        print("PWM VAL", duty_cycle)
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

def sweep_test(start, target):
    pwm_choice = 1
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

    duty_cycle = start
    print("PWM VAL", duty_cycle)
    while (abs(duty_cycle - target) > INCREMENT):
        pwm.start(duty_cycle)
        time.sleep(SLEEP)
        if (duty_cycle > target):
            duty_cycle -= INCREMENT
        else:
            duty_cycle += INCREMENT
        print(duty_cycle)

    pwm.stop()
    GPIO.cleanup()

if __name__ == "__main__":
    #sweep()
    num_tests = 100
    start = 0
    for t in range(0, num_tests):
        target = int(input("[+] Enter target [0-12]:"))
        sweep_test(start, target)
        start = target
        time.sleep(1)
