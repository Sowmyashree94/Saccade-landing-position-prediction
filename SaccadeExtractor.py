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

Vd = 130
Va = 30
Vf = 30

file = "/Users/niteeshmidlagajni/Downloads/Dataset-Original/P05_Recording.npy"
file1 = "/Users/niteeshmidlagajni/Documents/University/Third_sem/HCI/Docs/Saarland_data/Supplementary/DATA/GazeData/01_copy.tsv"

data = np.loadtxt(file1, delimiter='|')

data1 = np.load(file)

sampl_Freq = 300
window_length = 5


#
gazePosX_avg = (data[:,LeftGazePosition3dX]+data[:,RightGazePosition3dX])/2
gazePosY_avg = (data[:,LeftGazePosition3dY]+data[:,RightGazePosition3dY])/2

eyePosX_avg = (data[:,LeftEyePosition3dX]+data[:,RightEyePosition3dX])/2
eyePosY_avg = (data[:,LeftEyePosition3dY]+data[:,RightEyePosition3dY])/2

gazePosZ_avg = (data[:,LeftGazePosition3dZ]+data[:,RightGazePosition3dZ])/2
gaze_coordinates_3d = np.column_stack((gazePosX_avg,gazePosY_avg,gazePosZ_avg))
eyePosZ_avg = (data[:,LeftEyePosition3dZ]+data[:,RightEyePosition3dZ])/2
eye_coordinates_3d = np.column_stack((eyePosX_avg,eyePosY_avg, eyePosZ_avg))

time_stamps = data[:,Timestamp]

velocity = np.array([])

offset = math.floor(window_length/2)

window_length_index = window_length - 1

try:
    for i in range(0,len(gaze_coordinates_3d)):

        temp_a = gaze_coordinates_3d[i] - eye_coordinates_3d[i+offset]
        temp_b = gaze_coordinates_3d[i+window_length_index] -  eye_coordinates_3d[i+offset]
        time_diff = time_stamps[i+window_length_index] -  time_stamps[i]
        a = np.linalg.norm(temp_a)
        b =np.linalg.norm(temp_b)
        c =np.linalg.norm(temp_b - temp_a)
        coss = (a**2 + b**2 - c**2)/(2*a*b)
        coss = np.clip(coss, -1,1)
        alpha = math.degrees(math.acos(coss))
        velocity =  np.append(velocity, ((alpha)*1000000/time_diff))    
except:
    pass      



##-----------------------------------------------------------------------
velocity_filtered =savgol_filter(velocity,9,3)


time_stamps_cut = time_stamps[offset:-offset]

num_samples_anchor = math.ceil( 0.03/ (1/sampl_Freq))
count=0

saccade_timeStamps = np.array([]) #detection_point,anchor_point, final_point
saccade_indices = np.array([])
i = 0
while(i<len(velocity_filtered)):
    #Threshold velocity
    if velocity_filtered[i] >= Vd:
        #Go back in time to find anchor point
        temp_tstamps = np.array([time_stamps_cut[i]])
        temp_indices = np.array([i])
        found = False
        for j in range(i-1,i-num_samples_anchor,-1):
            if (velocity_filtered[j]==Va):
                #print("Saccade ",time_stamps_cut[j])
                count +=1
                found = True
                temp_tstamps = np.append(temp_tstamps, time_stamps_cut[j])
                temp_indices = np.append(temp_indices, j)
                break
            elif (velocity_filtered[j]>Va) and (velocity_filtered[j-1]<Va):
                # Interpolate to find timestamp where velocity could be Va
                x = [velocity_filtered[j-1],velocity_filtered[j]]
                y = [time_stamps_cut[j-1],time_stamps_cut[j]]
                interp_fn = interpolate.interp1d(x,y)
                temp_tstamps = np.append(temp_tstamps, interp_fn(Va))
                temp_indices = np.append(temp_indices, j)
                #print("Saccade ",interp_fn(Va)) 
                count +=1
                found = True
                break
            else:
                pass
        if found == True:           
            for k in range(i+1,len(velocity_filtered)):
                if (velocity_filtered[k]<Vf):
                    i = k
                    temp_tstamps = np.append(temp_tstamps, time_stamps_cut[k])
                    temp_indices = np.append(temp_indices, k)
                    break
            try:
                saccade_timeStamps = np.vstack((saccade_timeStamps,temp_tstamps))
                saccade_indices = np.vstack((saccade_indices,temp_indices))
            except:
                try:
                    saccade_timeStamps = np.hstack((saccade_timeStamps,temp_tstamps))
                    saccade_indices = np.hstack((saccade_indices,temp_indices))
                except:
                    pass
    i += 1
                
print(count)               
            


#---------------------------------------------------------------------------------------------

num = 50

indices_range = [int(saccade_indices[num,1]),int(saccade_indices[num,2])]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(time_stamps_cut[indices_range[0]-10:indices_range[1]+10] , velocity_filtered[indices_range[0]-10:indices_range[1]+10])

xcoords = [saccade_timeStamps[num,0], saccade_timeStamps[num,1], saccade_timeStamps[num,2]]
colors = ['r','k','b']
labels =['Detection pt Vd = %i deg/s'%Vd,'Anchor pt Va = %i deg/s'%Va,'Final pt Vf = %i deg/s'%Vf]

for xc,c,l in zip(xcoords,colors,labels):
    plt.axvline(x=xc, label=l, c=c)

plt.legend()

plt.xlabel("Time in Microseconds")
plt.ylabel("Velocity in degrees/second")

plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(time_stamps_cut[500:1000,],velocity_filtered[500:1000],)
plt.title("Velocity plot with filtered data")
plt.xlabel("Time in Microseconds")
plt.ylabel("Velocity in degrees/second")

plt.show()


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(time_stamps_cut[500:1000,],velocity[500:1000],)
plt.title("Velocity plot with raw data")
plt.xlabel("Time in Microseconds")
plt.ylabel("Velocity in degrees/second")

plt.show()
