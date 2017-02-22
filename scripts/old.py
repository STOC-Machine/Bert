from __future__ import division
import time,sys,getopt
import Adafruit_PCA9685
import operator
import math
import socket
import RTIMU

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(300)

MAX_VAL = 1000
MIN_VAL = 200

IMU_IP = "127.0.0.2"
IMU_PORT = 5005
SETTINGS_FILE = "RTIMULib"

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
imu.IMUInit()
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
#imu.setAccelEnable(True)

poll_interval = imu.IMUGetPollInterval()

#declare data variables
roll = 0.0
pitch = 0.0

def calibrate():
  #calibrate ESCs in slots 0,1,2,3
  pwm.set_pwm(0,0,MAX_VAL)
  pwm.set_pwm(1,0,MAX_VAL)
  pwm.set_pwm(2,0,MAX_VAL)
  pwm.set_pwm(3,0,MAX_VAL)
  time.sleep(0.5)

def main():
  #calibrate()
  on = True
  while on:
    data = imu.getIMUData()
    fusionPose = data["fusionPose"]
    Gyro = data["gyro"]
    roll = round(math.degrees(fusionPose[0]),1)
    pitch = round(math.degrees(fusionPose[1]),1)
    print roll
    print pitch

main()

