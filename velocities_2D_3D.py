#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 18:09:40 2018

@author: niteeshmidlagajni
"""

from scipy.signal import savgol_filter
from scipy import interpolate, optimize
import numpy as np
import math
from math import atan2, degrees
import matplotlib.pyplot as plt

LeftGazePosition2dX = 0
LeftGazePosition2dY= 1
RightGazePosition2dX=2
RightGazePosition2dY= 3
LeftGazePosition3dX= 4
LeftGazePosition3dY= 5
LeftGazePosition3dZ= 6
RightGazePosition3dX= 7
RightGazePosition3dY= 8
RightGazePosition3dZ= 9
LeftEyePosition3dX= 10
LeftEyePosition3dY= 11
LeftEyePosition3dZ= 12
RightEyePosition3dX=13
RightEyePosition3dY= 14
RightEyePosition3dZ= 15
Timestamp= 16
LeftValidity=17
RightValidity= 18
LeftPupil= 19
RightPupil= 20
display = [2560,1440] 

Vd = 130
Va = 30
Vf = 30

#file = "/Users/niteeshmidlagajni/Downloads/Dataset-Original/P05_Recording.npy"
file = "/home/niteesh/Documents/uni/HCI/Saarland/Supplementary/DATA/GazeData/01.tsv"

data = np.genfromtxt(file, skip_header=1, delimiter='|')


sampl_Freq = 300
window_length = 5
distance_frmMonitor = 70 #in cm
ScreenWidth = 60.77 #cms excluding bezel width
dispHoriRes = 2560

deg_per_px = degrees(atan2(.5*ScreenWidth, distance_frmMonitor)) / (.5*dispHoriRes)
 
gazePosX_avg = ((data[:,LeftGazePosition2dX]+data[:,RightGazePosition2dX])/2)*display[0]

gazePosY_avg = ((data[:,LeftGazePosition2dY]+data[:,RightGazePosition2dY])/2)*display[1]


gaze_coordinates_3d = np.column_stack((gazePosX_avg,gazePosY_avg))


time_stamps = data[:,Timestamp]

velocity = np.array([])
velocity1 = np.array([])

offset = math.floor(window_length/2)

gazePosX_avg = (data[:,LeftGazePosition3dX]+data[:,RightGazePosition3dX])/2
gazePosY_avg = (data[:,LeftGazePosition3dY]+data[:,RightGazePosition3dY])/2

eyePosX_avg = (data[:,LeftEyePosition3dX]+data[:,RightEyePosition3dX])/2
eyePosY_avg = (data[:,LeftEyePosition3dY]+data[:,RightEyePosition3dY])/2

gazePosZ_avg = (data[:,LeftGazePosition3dZ]+data[:,RightGazePosition3dZ])/2
gaze_coordinates_3d1 = np.column_stack((gazePosX_avg,gazePosY_avg,gazePosZ_avg))
eyePosZ_avg = (data[:,LeftEyePosition3dZ]+data[:,RightEyePosition3dZ])/2
eye_coordinates_3d1 = np.column_stack((eyePosX_avg,eyePosY_avg, eyePosZ_avg))

try:
    for i in range(offset,len(gaze_coordinates_3d) - offset):

        diff = gaze_coordinates_3d[i+offset] - gaze_coordinates_3d[i-offset]       
        dist = np.linalg.norm(diff)
        v = ((dist * deg_per_px) * sampl_Freq)/(2*offset)
        velocity =  np.append(velocity, v)  
        
        temp_a = gaze_coordinates_3d1[i+offset]  - eye_coordinates_3d1[i]
        temp_b = gaze_coordinates_3d1[i-offset] - eye_coordinates_3d1[i]
        a = np.linalg.norm(temp_a)
        b =np.linalg.norm(temp_b)
        c =np.linalg.norm(temp_b - temp_a)
        coss = (a**2 + b**2 - c**2)/(2*a*b)
        coss = np.clip(coss, -1,1)
        alpha = math.degrees(math.acos(coss))
        velocity1 =  np.append(velocity1, ((alpha)*sampl_Freq/(2*offset)))
except:
    pass      
    


##-----------------------------------------------------------------------
velocity_filtered =savgol_filter(velocity,9,3)
velocity_filtered1 =savgol_filter(velocity1,9,3)


#---------------------------------------------------------------------------------------------

num = 50

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(velocity_filtered[300:1000],label="With 2D gaze data")
ax.plot(velocity_filtered1[300:1000],label="With 3D gaze data")
plt.xlabel("samples")
plt.ylabel("Velocity in degrees/second")
plt.legend()
plt.show()

