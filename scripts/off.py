from __future__ import division
import time, curses
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(300)

pwm.set_pwm(0,0,0)
pwm.set_pwm(1,0,0)
pwm.set_pwm(2,0,0)
pwm.set_pwm(3,0,0)
