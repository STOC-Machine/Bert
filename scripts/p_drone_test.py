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
PCOF = 0.06
   
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
front_motors = [0,2]
back_motors = [1,3]
left_motors = [0,1]
right_motors = [2,3]

def calibrate():
  for motor in motors:
    pwm.set_pwm(motor,0,MAX_VAL)
  time.sleep(0.5)

def main():
  start = 1
  
  print("calibrating...")
  calibrate()
  
  print("Sleeping")
  time.sleep(2)
  
  print("testing")
  spd_0 = BASE_SPEED
  spd_1 = BASE_SPEED
  spd_2 = BASE_SPEED
  spd_3 = BASE_SPEED

  while True:  
    hack = time.time()    
   
    if imu.IMURead():  
      data = imu.getIMUData()  
      fusionPose = data["fusionPose"]    
   
      if (hack - t_damp) > .1:  
        roll = round(math.degrees(fusionPose[0]), 1)  
        pitch = round(math.degrees(fusionPose[1]), 1)
        if roll < 0:
          roll = (180 - abs(roll)) + 180 
        if start == 1:
          rollinit = roll
          pitchinit = pitch
          start = 0
        #print("Roll is " + str(roll))
        #print("Pitch is " + str(pitch))

      roll_error = round(rollinit - roll)
      pitch_error = pitchinit - pitch
      
      #print(roll_error)
      spd_0 -= PCOF * roll_error
      spd_1 -= PCOF * roll_error
      spd_2 += PCOF * roll_error
      spd_3 += PCOF * roll_error
      #print(spd_0)
      #spd_0 += PCOF * pitch_error
      #spd_1 -= PCOF * pitch_error
      #spd_2 += PCOF * pitch_error
      #spd_3 -= PCOF * pitch_error

      pwm.set_pwm(0,0,int(spd_0))
      pwm.set_pwm(1,0,int(spd_1))
      pwm.set_pwm(2,0,int(spd_2))
      pwm.set_pwm(3,0,int(spd_3))   
main()

