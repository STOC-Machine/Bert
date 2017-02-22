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
MAX_SPEED = 230
BASE_SPEED = 220    
PCOF = 0.5
PCOF_P = 0.9
ICOF = 0.002
ICOF_P = 0.002

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
  rolltot = 0
  pitchtot = 0
  rollinit = 0
  pitchinit = 0
  
  #print("calibrating...")
  calibrate()
  
  print("Sleeping")
  time.sleep(2)
  n = 0
  print("testing")
  spd_0 = BASE_SPEED
  spd_1 = BASE_SPEED
  spd_2 = BASE_SPEED
  spd_3 = BASE_SPEED

  ##To be used to see if the speeds are in an acceptable range##
  check0=0
  check1=0
  check2=0
  check3=0

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

      roll_error = round(rollinit - roll)
      pitch_error = round(pitchinit - pitch)
      #print(roll)
      #print(pitch_error)
      #print(pitchinit)

      rolltot += roll_error
      pitchtot += pitch_error
      
      Iterm_roll = ICOF * rolltot
      #print(Iterm_roll)
      Pterm_roll = PCOF * roll_error

      Iterm_pitch = ICOF_P * pitchtot
      Pterm_pitch = PCOF_P * pitch_error

      check0 = spd_0 - Pterm_roll - Pterm_pitch
      check1 = spd_1 - Pterm_roll + Pterm_pitch
      check2 = spd_2 + Pterm_roll - Pterm_pitch
      check3 = spd_3 + Pterm_roll + Pterm_pitch

      #print("Error: " + str(pitch_error))
      if int(check0) in range(MIN_VAL,MAX_SPEED):    	
      	spd_0 = check0

      if int(check1) in range(MIN_VAL,MAX_SPEED):
	spd_1 = check1

      if int(check2) in range(MIN_VAL,MAX_SPEED):
	spd_2 = check2	

      if int(check3) in range(MIN_VAL,MAX_SPEED):
	spd_3 = check3   

      print("0 is " + str(int(spd_0)))
      print("1 is " + str(int(spd_1)))
      print("2 is " + str(int(spd_2)))
      print("3 is " + str(int(spd_3)))

      if int(spd_0) in range(MIN_VAL,MAX_SPEED):
        pwm.set_pwm(0,0,int(spd_0))
      if int(spd_1) in range(MIN_VAL,MAX_SPEED):
        pwm.set_pwm(1,0,int(spd_1))
      if int(spd_2) in range(MIN_VAL,MAX_SPEED):
        pwm.set_pwm(2,0,int(spd_2))
      if int(spd_3) in range(MIN_VAL,MAX_SPEED):
        pwm.set_pwm(3,0,int(spd_3))   
main()

