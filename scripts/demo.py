from __future__ import division
import sys, getopt  
import RTIMU  
import time  
import math
from random import randint
import Adafruit_PCA9685
sys.path.append('.')

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(300)

MAX_VAL = 1000
MIN_VAL = 180
BASE_SPEED = 220    
P_COFF = 1

   
SETTINGS_FILE = "RTIMULib"  
   
s = RTIMU.Settings(SETTINGS_FILE)  
imu = RTIMU.RTIMU(s)  
   
# timer    
t_damp = time.time() 
   
if (not imu.IMUInit()):
  print("Failed to initialize IMU")  
   
imu.setSlerpPower(0.02)  
imu.setGyroEnable(True)  
#imu.setAccelEnable(True)  
#imu.setCompassEnable(True)  

# data variables  
roll = 0.0  
pitch = 0.0

motors = [0,1,2,3]
front_motors = []
back_motors = []
left_motors = []
right_motors = []

def calibrate():
  for motor in motors:
    pwm.set_pwm(motor,0,MAX_VAL)
  time.sleep(0.5)

def main():
  start = 1
  print("calibrating...")
  calibrate()
  #for motor in motors:
  #  pwm.set_pwm(motor,0,0)
  #time.sleep(1)
  print("Sleeping")
  time.sleep(2)
  print("testing")
  for motor in motors:
    pwm.set_pwm(motor,0,MIN_VAL)
    print motor
    time.sleep(1)
    pwm.set_pwm(motor,0,0)

  while True:  
    hack = time.time()    
   
    if imu.IMURead():  
      data = imu.getIMUData()  
      fusionPose = data["fusionPose"]    
   
      if (hack - t_damp) > .1:  
        roll = round(math.degrees(fusionPose[0]), 1)  
        pitch = round(math.degrees(fusionPose[1]), 1)
        if start == 1:
          rollinit = roll
          pitchinit = pitch
          start = 0
        print("Roll is " + str(roll))
        print("Pitch is " + str(pitch))

      roll_error = rollinit - roll
    

main()
