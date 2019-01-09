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
import filepath

timee = time.time()

GazePosition2dX = 0
GazePosition2dY = 1
Timestamp= 2
Vd = 130
Va = 60
Vf = 60
sampl_Freq = 65
window_length = 3       
display = [1920,1080]                                                                                                                                                                              

distance_frmMonitor = 63 #in cm
ScreenWidth = 53 #cms excluding bezel width
dispHoriRes = 1920

min_saccade_samples = 10 #With this parameter, only saccades longer than it are recorded
num_samples_train = 10 #For every saccade, only first num_samples_train are stored in npy file for training

deg_per_px = math.degrees(math.atan2(.5*ScreenWidth, distance_frmMonitor)) / (.5*dispHoriRes)


data_dir = filepath.filepath_eyeX
files = os.listdir(data_dir)
files.sort()

velocities_allUsrs = [] #contains velocities from all users, length is # of users
SaccadeIndices_allUsrs = [] #contains saccade indices from all users, length is # of users
SaccadeTimeStamps_allUsrs = [] #contains time_stamps from all users, length is # of users

#for f in files:
#file = data_dir + "/" + f
#file = data_dir + "/" + "data_test_07012019_18_25.txt"
file = filepath.filepath_eyeX

data = np.genfromtxt(file, delimiter='|')

#file1 = data_dir + "/" + "g_truth.txt"
file1 = filepath.filepath_pyGame
data1 = np.genfromtxt(file1, delimiter='')

data_out_dir = filepath.path_npy
subject_count = 1
#-------------------------------------------------------------------------------------------------------------

distances = []

for i in range(1,len(data1)):
    te = data1[i]-data1[i-1]
    te = np.linalg.norm(te)
    distances.append(te)



#--------------------------------------------------------------------------------------------------------

gazePosX_avg = data[:,GazePosition2dX]
gazePosY_avg = data[:,GazePosition2dY]

gaze_coordinates_2d = np.column_stack((gazePosX_avg,gazePosY_avg))

gaze_coordinates_2d1 =gaze_coordinates_2d/display
#take only in range 0 to 1    
mask = (gaze_coordinates_2d1 >= 0) & (gaze_coordinates_2d1 <= 1)
for i,m in enumerate(mask):
    mask[i] = m.all()
mask = mask[:,0]
gaze_coordinates_2d1 =gaze_coordinates_2d1[mask]
gaze_coordinates_2d =gaze_coordinates_2d[mask]

#time_stamps = data[:,Timestamp]

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
velocity_filtered =savgol_filter(velocity,13,4)


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
                    offset_15ms_glissades = math.ceil((15*10**-3) * sampl_Freq)
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

#take saccades with minimn number of samples equals 10 
temp_numSamples = saccade_indices[:,2] -saccade_indices[:,0]
mask1 = temp_numSamples >= min_saccade_samples
saccade_indices = saccade_indices[mask1]

SaccadeIndices_allUsrs.append(saccade_indices)
SaccadeTimeStamps_allUsrs.append(saccade_timeStamps)

data_out = np.array([])
for e in range(0,len(saccade_indices)):
    start = int(saccade_indices[e,0])
    end = int(saccade_indices[e,2])
    temp_stream = gaze_coordinates_2d1[start-offset:end-offset+1]
    temp_stream = np.hstack((temp_stream, velocity_filtered[start:end+1].reshape((temp_stream.shape[0],1))))
    if(temp_stream.shape[0] >= num_samples_train):
        temp_stream = temp_stream[0:num_samples_train]
    else:
        #this case will not come when mask applied for min saccade length
        temp_stream = np.pad(temp_stream,((0,num_samples_train-temp_stream.shape[0]),(0,0)), 'constant',constant_values=(np.inf,))
    temp_last = np.append(gaze_coordinates_2d1[end-offset+1],0)
    temp_stream = np.vstack((temp_stream, temp_last))
    temp_stream = temp_stream.reshape((1,num_samples_train+1,3))
    if e != 0:
        data_out = np.vstack((data_out,temp_stream))
    else:
        data_out = np.copy(temp_stream)
np.save(data_out_dir+str(subject_count),data_out)
subject_count += 1
        
       
print("saccades",count)     
print("Not saccades",count_notsaccades)           
                


#---------------------------------------------------------------------------------------------

num = 0
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
ax.plot(velocities_allUsrs[user][:])
plt.title("Velocity plot for data extracted from EyeX")
plt.xlabel("Samples")
plt.ylabel("Velocity in degrees/second")
plt.show()

#fig = plt.figure()
#ax = fig.add_subplot(111)
#x1 = 2802
#y1 = 2815
#ax.plot(gaze_coordinates_2d[x1:y1,0],gaze_coordinates_2d[x1:y1,1])
#plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
ax.bar(range(0,len(distances)),distances)
plt.title("Bar chart showing L2 distance between 2 points in pygame App")
plt.xlabel("Sequence")
plt.ylabel("Distance")
plt.show()

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.hist(velocities_allUsrs[user][indices_range[0]:indices_range[1]])
#plt.show()
#--------------------------------------------------------------------------------------------------------------
#saccade analysis

saccade_length = SaccadeIndices_allUsrs[user][:,2] - SaccadeIndices_allUsrs[user][:,1]
print("\n\nAverage saccade duration is %f samples with a high of %i and low of %i\n"%(saccade_length.mean(),saccade_length.max(),saccade_length.min()))
time_per_sample = (1/sampl_Freq)*1000 #ms
print("Average saccade duration in time is %fms with a high of %ims and low of %ims\n"%(saccade_length.mean()*time_per_sample,saccade_length.max()*time_per_sample,saccade_length.min()*time_per_sample))