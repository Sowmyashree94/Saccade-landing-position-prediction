# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 11:20:22 2019

@author: Niteesh
"""
import datetime
import os

basepath = r"F:\HCI\EyeX_data"
date = datetime.datetime.now().strftime("%d%m%Y")
users = ["Niteesh","Sowmya","Trap"]
user_Number = 1

date_dir = basepath +"\\"+  date
if not os.path.exists(date_dir):
    os.makedirs(date_dir)
    
user_dir = date_dir +"\\"+ users[user_Number]
if not os.path.exists(user_dir):
    os.makedirs(user_dir)

user_dir_data = user_dir + "\\data"
user_dir_gtruth = user_dir + "\\gtruth"
if not os.path.exists(user_dir_data):
    os.makedirs(user_dir_data)
if not os.path.exists(user_dir_gtruth):
    os.makedirs(user_dir_gtruth)

filepath_eyeX = user_dir_data +"\data_test_"  +datetime.datetime.now().strftime("%d%m%Y_%H_%M") +".txt"

filepath_pyGame = user_dir_gtruth +"\g_truth_"  +datetime.datetime.now().strftime("%d%m%Y_%H_%M") +".txt"

path_npy = user_dir + "\\npy"



if not os.path.exists(path_npy):
    os.makedirs(path_npy)
