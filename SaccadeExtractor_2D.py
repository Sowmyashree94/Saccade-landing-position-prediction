#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 18:09:40 2018

@author: niteeshmidlagajni
"""

from scipy.signal import savgol_filter
from scipy import interpolate
import os
import numpy as np
import math
import matplotlib.pyplot as plt
import time
from mpl_toolkits.mplot3d.axes3d import Axes3D

timee = time.time()

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
Va = 60
Vf = 60
sampl_Freq = 300
window_length = 5    
num_samples_train = 15   
display = [2560,1440]   
                                                                                                                                                                           

distance_frmMonitor = 70 #in cm
ScreenWidth = 60.77 #cms excluding bezel width
dispHoriRes = 2560

deg_per_px = math.degrees(math.atan2(.5*ScreenWidth, distance_frmMonitor)) / (.5*dispHoriRes)


data_dir = "/home/niteesh/Documents/uni/HCI/Saarland/Supplementary/DATA/GazeData"
files = os.listdir(data_dir)
files.sort()

velocities_allUsrs = [] #contains velocities from all users, length is # of users
SaccadeIndices_allUsrs = [] #contains saccade indices from all users, length is # of users
SaccadeTimeStamps_allUsrs = [] #contains time_stamps from all users, length is # of users

data_out_dir = "/home/niteesh/Documents/uni/HCI/Saarland/Npy_files/"
subject_count = 1


for f in files:
    file = data_dir + "/" + f
    data = np.genfromtxt(file, skip_header=1, delimiter='|')
    
    gazePosX_avg = ((data[:,LeftGazePosition2dX]+data[:,RightGazePosition2dX])/2)*display[0]
    gazePosY_avg = ((data[:,LeftGazePosition2dY]+data[:,RightGazePosition2dY])/2)*display[1]

    gaze_coordinates_2d = np.column_stack((gazePosX_avg,gazePosY_avg))
    
    time_stamps = data[:,Timestamp]
    
    velocity = np.array([])
    
    offset = math.floor(window_length/2)
    
    
    try:
        for i in range(offset,len(gaze_coordinates_2d) - offset):
            
            diff = gaze_coordinates_2d[i+offset] - gaze_coordinates_2d[i-offset]       
            dist = np.linalg.norm(diff)
            v = ((dist * deg_per_px) * sampl_Freq)/(2*offset)
            velocity =  np.append(velocity, v) 
            
            temp_a = gaze_coordinates_2d[i+offset]
            temp_b = gaze_coordinates_2d[i-offset]
            time_diff = time_stamps[i+offset] -  time_stamps[i-offset]
            
    except:
        pass      
    
    ##-----------------------------------------------------------------------
    velocity_filtered =savgol_filter(velocity,9,3)

    
    velocities_allUsrs.append(velocity_filtered)
    
    time_stamps_cut = time_stamps[offset:-offset]
    
    num_samples_anchor = math.ceil( 0.03/ (1/sampl_Freq))
    count=0
    count_notsaccades = 0
    
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
                    count +=1
                    found = True
                    break
                else:
                    pass
            if found == True:           
                for k in range(i+1,len(velocity_filtered)):
                    if (velocity_filtered[k]<Vf):
                        offset_15ms_glissades = math.floor((15*10**-3) * sampl_Freq)
                        k += offset_15ms_glissades
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
            else:
                count_notsaccades +=1
        i += 1
    
    
    SaccadeIndices_allUsrs.append(saccade_indices)
    SaccadeTimeStamps_allUsrs.append(saccade_timeStamps)
    
    data_out = np.array([])
    for e in range(0,len(saccade_indices)):
        temp_stream = gaze_coordinates_2d[int(saccade_indices[e,0])-offset:int(saccade_indices[e,2]-offset+1)]
        if(temp_stream.shape[0] >= num_samples_train):
            temp_stream = temp_stream[0:num_samples_train]
        else:
            temp_stream = np.pad(temp_stream,((0,num_samples_train-temp_stream.shape[0]),(0,0)), 'constant',constant_values=(np.nan,))
        temp_stream = temp_stream.reshape((1,num_samples_train,2))
        if e != 0:
            data_out = np.vstack((data_out,temp_stream))
        else:
            data_out = np.copy(temp_stream)
    np.save(data_out_dir+str(subject_count),data_out)
    subject_count += 1
        

           
    print("saccades",count)     
#    print("Not saccades",count_notsaccades)        
                


#---------------------------------------------------------------------------------------------

num = 367
user = 0
#
indices_range = [int(SaccadeIndices_allUsrs[user][num,1]),int(SaccadeIndices_allUsrs[user][num,2])]
#
fig = plt.figure()
ax = fig.add_subplot(111)
#ax.plot(time_stamps_cut[indices_range[0]-10:indices_range[1]+10] , velocity_filtered[indices_range[0]-10:indices_range[1]+10])
#ax.plot(velocities_allUsrs[user][indices_range[0]-10:indices_range[1]+10])
ax.plot(velocities_allUsrs[user][indices_range[0]:indices_range[1]])

#xcoords = [SaccadeTimeStamps_allUsrs[user][num,0], SaccadeTimeStamps_allUsrs[user][num,1], SaccadeTimeStamps_allUsrs[user][num,2]]
#colors = ['r','k','b']
#labels =['Detection pt Vd = %i deg/s'%Vd,'Anchor pt Va = %i deg/s'%Va,'Final pt Vf = %i deg/s'%Vf]

#for xc,c,l in zip(xcoords,colors,labels):
#    plt.axvline(x=xc, label=l, c=c)

#plt.legend()
plt.xlabel("Time in Microseconds")
plt.ylabel("Velocity in degrees/second")
plt.show()
#
##fig = plt.figure()
##ax = fig.add_subplot(111)
##ax.plot(time_stamps_cut[500:1000,],velocity_filtered[500:1000],)
##plt.title("Velocity plot with filtered data")
##plt.xlabel("Time in Microseconds")
##plt.ylabel("Velocity in degrees/second")
##plt.show()
##
##
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(velocities_allUsrs[user])
plt.title("Velocity plot with raw data")
plt.xlabel("Time in Microseconds")
plt.ylabel("Velocity in degrees/second")
plt.show()


fig = plt.figure()
ax = fig.add_subplot(111)
ax.hist(velocities_allUsrs[user][indices_range[0]:indices_range[1]])
plt.show()

saccade_length = SaccadeIndices_allUsrs[user][:,2] - SaccadeIndices_allUsrs[user][:,0]
print("\n\nAverage saccade duration is %f samples with a high of %i and low of %i\n"%(saccade_length.mean(),saccade_length.max(),saccade_length.min()))
time_per_sample = (1/sampl_Freq)*1000 #ms
print("Average saccade duration in time is %fms with a high of %ims and low of %ims\n"%(saccade_length.mean()*time_per_sample,saccade_length.max()*time_per_sample,saccade_length.min()*time_per_sample))

print("TIME   ",time.time() - timee)

#---------------------------------------------------------------------------------------------


