import sys, getopt     
sys.path.append('.')  
import RTIMU  
import os.path  
import time  
import math  
import operator  
import socket    
   
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
   
while True:  
  hack = time.time()    
   
  if imu.IMURead():  
   data = imu.getIMUData()  
   fusionPose = data["fusionPose"]    
   
   if (hack - t_damp) > .1:  
     roll = round(math.degrees(fusionPose[0]), 1)  
     pitch = round(math.degrees(fusionPose[1]), 1)
     print(roll)
