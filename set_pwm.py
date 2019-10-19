#!/usr/bin/python3

import RPi.GPIO as GPIO
import time, sys, os

PWM0_PIN = 12
PWM1_PIN = 13

def set_pwm(x, y, seconds=1):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PWM0_PIN, GPIO.OUT)
    GPIO.setup(PWM1_PIN, GPIO.OUT)
    pwmX = GPIO.PWM(PWM0_PIN, 50)
    pwmY = GPIO.PWM(PWM1_PIN, 50)
    convertedX = (x*10/180.0)
    convertedY = (y*10/180.0)
    print("PWM SET TO %f, %f" % (convertedX, convertedY))

    pwmX.stop()
    pwmY.stop()
    GPIO.cleanup()

def main():
    if (len(sys.argv) != 4):
        print("USAGE: test_pwm.py <pwm> <duty_cycle> <seconds>")
        exit(1)
    pwm_choice = int(sys.argv[1])
    duty_cycle = float(sys.argv[2])
    seconds    = float(sys.argv[3])
    print("PWM %d at %f for %f seconds" % (pwm_choice, duty_cycle, seconds))


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

if __name__ == "__main__":
    main()
