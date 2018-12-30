#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 18:09:40 2018

@author: niteeshmidlagajni
"""

import os
import numpy as np
import math
import matplotlib.pyplot as plt
import time
from scipy.ndimage.interpolation import shift


class DecisionEngine:
    
    def __init__(self, sampl_Freq, distance_frmMonitor, display_resolution, ScreenWidth, lstm_length, features_lstm, Vd = 130, Vf=60, window_length = 5):
        self.Vd = Vd
        self.Vf=Vf
        self.window_length = window_length
        self.lstm_length =lstm_length
        self.features = features_lstm
        self.gaze_data_array = np.array([])
        self.deg_per_px = math.degrees(math.atan2(.5*ScreenWidth, distance_frmMonitor)) / (.5*display_resolution[0])
        self.velocity_mult = (self.deg_per_px* sampl_Freq)/(2*(math.floor(self.window_length/2)))

        self.offset_15ms_glissades = math.floor((15*10**-3) * sampl_Freq)
        self.states = {0:"Init",
                  1:"Normal_op",
                  2:"Collect_forLSTM",
                  3:"Predict",
                  4:"EndPrediction"}  
      
        self.state = self.states[0]
        self.count_samplesAfterVf = 0

    def calculate_velocity(self, gaze_start, gaze_end):
        diff = gaze_end - gaze_start       
        dist = np.linalg.norm(diff)
        v = dist * self.velocity_mult
        return v
              
    def evaluate_ThresholdVelocity(self, velocity):
        return velocity >= self.Vd
    
    def evaluate_FinalVelocity(self, velocity):
        return velocity <= self.Vf
        
    def update_gazeArray(self, gaze_data_array,gaze_coordinate_2d):
        local_gaze = np.roll(gaze_data_array,-1,axis=0)
        local_gaze[-1] = gaze_coordinate_2d
        return local_gaze 
          
    
    def run_engine(self, gaze_coordinate_2d,gaze_coordinate_2d1): 
        print(self.state)
        if self.state == 'Init':
            if self.gaze_data_array.size == 0:
                 self.gaze_data_array = gaze_coordinate_2d
            else:
                self.gaze_data_array = np.vstack((self.gaze_data_array,gaze_coordinate_2d))

            if self.gaze_data_array.shape[0] == self.window_length:
                self.state = self.states[1]
                velocity = self.calculate_velocity(self.gaze_data_array[0],self.gaze_data_array[-1])  
        else:
            self.gaze_data_array = self.update_gazeArray(self.gaze_data_array,gaze_coordinate_2d)  
            velocity = self.calculate_velocity(self.gaze_data_array[0],self.gaze_data_array[-1])         
            print(velocity)
            if self.state == 'Normal_op':   
                if self.evaluate_ThresholdVelocity(velocity):
                    self.state = self.states[2]
                    gaze_toLstm = np.array([gaze_coordinate_2d1])
        
            elif self.state == 'Collect_forLSTM':  
                gaze_toLstm = np.append(gaze_toLstm, gaze_coordinate_2d1)   
                if gaze_toLstm.shape[0] == self.lstm_length:
                    self.state = self.states[3]
                    gaze_toLstm.reshape((1,self.lstm_length,self.features))
                    
            elif self.state == 'Predict':   
#                temp_gaze = model.predict(gaze_toLstm)
#                gaze_coordinate_2d = temp_gaze
                if self.evaluate_FinalVelocity(velocity):
                    self.count_samplesAfterVf = 0
                    self.state = self.states[4]
                    
            elif self.state == 'EndPrediction':   
                self.count_samplesAfterVf +=1
#                temp_gaze = model.predict(gaze_toLstm)
#                gaze_coordinate_2d = temp_gaze
                if self.count_samplesAfterVf == self.offset_15ms_glissades:
                    self.state = self.states[1]        
            else:
                #will never come to this
                pass
         
        return gaze_coordinate_2d

#def main():
test = DecisionEngine( Vd = 130, 
                          Vf=60, 
                          window_length = 5, 
                           sampl_Freq =300, 
                           distance_frmMonitor =70,
                           ScreenWidth = 60.77,
                           display_resolution = [2560,1440] , 
                           lstm_length = 10, 
                           features_lstm = 3 
                    )

file = r"F:\HCI\data\01.tsv"
LeftGazePosition2dX = 0
LeftGazePosition2dY= 1
RightGazePosition2dX=2
RightGazePosition2dY= 3
data = np.genfromtxt(file, skip_header=1, delimiter='|')

gazePosX_avg = ((data[:,LeftGazePosition2dX]+data[:,RightGazePosition2dX])/2)*2560
gazePosY_avg = ((data[:,LeftGazePosition2dY]+data[:,RightGazePosition2dY])/2)*1440

gazePosX_avg1 = ((data[:,LeftGazePosition2dX]+data[:,RightGazePosition2dX])/2)
gazePosY_avg1 = ((data[:,LeftGazePosition2dY]+data[:,RightGazePosition2dY])/2)

gaze_coordinates_2d = np.column_stack((gazePosX_avg,gazePosY_avg))
gaze_coordinates_2d1 = np.column_stack((gazePosX_avg1,gazePosY_avg1))

gaze_coordinates_2da = gaze_coordinates_2d[500:800]
gaze_coordinates_2d1a = gaze_coordinates_2d1[500:800]
for i in range(0,200):
    test.run_engine(gaze_coordinates_2da[i].reshape(1,2),gaze_coordinates_2d1a[i].reshape(1,2))

        
#if __name__ == "__main__":
#        main()
