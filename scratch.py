#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 18:09:40 2018

@author: niteeshmidlagajni
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 12:00:35 2018

@author: niteeshmidlagajni
"""
from scipy.signal import savgol_filter
import numpy as np
import math
import matplotlib.pyplot as plt

LeftGazePosition2dX = 0
LeftGazePosition2dY = 1
RightGazePosition2dX = 2
RightGazePosition2dY = 3
LeftGazePosition3dX = 4
LeftGazePosition3dY = 5
LeftGazePosition3dZ = 6
RightGazePosition3dX = 7
RightGazePosition3dY = 8
RightGazePosition3dZ = 9
LeftEyePosition3dX = 10
LeftEyePosition3dY = 11
LeftEyePosition3dZ = 12
RightEyePosition3dX =13
RightEyePosition3dY = 14
RightEyePosition3dZ = 15
Timestamp = 16
LeftValidity =17
RightValidity = 18
LeftPupil = 19
RightPupil = 20

# file = "/Users/niteeshmidlagajni/Downloads/Dataset-Original/P05_Recording.npy"
file1 = "D:/Datasets/HCI_Supplementary/DATA/GazeData/01.tsv"

data = np.loadtxt(file1, delimiter='|')

#data1 = np.load(file)

samFreq = 300
window_length = 5


#
gazePosX_avg = (data[:,LeftGazePosition3dX]+data[:,RightGazePosition3dX])/2
gazePosY_avg = (data[:,LeftGazePosition3dY]+data[:,RightGazePosition3dY])/2

eyePosX_avg = (data[:,LeftEyePosition3dX]+data[:,RightEyePosition3dX])/2
eyePosY_avg = (data[:,LeftEyePosition3dY]+data[:,RightEyePosition3dY])/2
#
gaze_coordinates = np.column_stack((gazePosX_avg,gazePosY_avg))
eye_coordinates = np.column_stack((eyePosX_avg,eyePosY_avg))

gazePosZ_avg = (data[:, LeftGazePosition3dZ]+data[:,RightGazePosition3dZ])/2
gaze_coordinates_3d = np.column_stack((gazePosX_avg,gazePosY_avg,gazePosZ_avg))
eyePosZ_avg = (data[:,LeftEyePosition3dZ]+data[:,RightEyePosition3dZ])/2
eye_coordinates_3d = np.column_stack((eyePosX_avg,eyePosY_avg, eyePosZ_avg))

time_stamps = data[:, Timestamp]

velocity = []

offset = math.ceil(window_length/2)

window_length_index = window_length - 1

try:
    for i in range(0,len(gaze_coordinates)):
        temp_a = gaze_coordinates_3d[i] - eye_coordinates_3d[i+offset]
        temp_b = gaze_coordinates_3d[i+window_length_index] -  eye_coordinates_3d[i+offset]
        time_diff = time_stamps[i+window_length_index] -  time_stamps[i]
        a = np.linalg.norm(temp_a)
        b = np.linalg.norm(temp_b)
        c = np.linalg.norm(temp_b - temp_a)
        coss = (a**2 + b**2 - c**2)/(2*a*b)
        coss = np.clip(coss, -1,1)
        alpha = math.degrees(math.acos(coss))
        velocity.append((alpha)*1000000/time_diff)    
except:
    pass      


##-----------------------------------------------------------------------
e =savgol_filter(velocity,9,3)


count_e = 0

for i in e:
    if i >100:
        count_e += 1
        
print(count_e)

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.plot(velocity)
#plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(e[500:1000])
plt.show()
