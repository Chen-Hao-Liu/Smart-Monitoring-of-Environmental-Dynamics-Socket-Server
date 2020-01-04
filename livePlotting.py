# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:48:04 2019

@author: Chen Hao
"""

import matplotlib.pyplot as plt
import numpy as np
import socket;
import sys;
#import matplotlib.animation as animation
#-------------------------------------
# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

#'192.168.207.73' Winlab

#replace with the current ip
HOST = '192.168.207.73';
PORT = 6000;

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#socket.socket: must use to create a socket.
#socket.AF_INET: Address Format, Internet = IP Addresses.
#socket.SOCK_STREAM: two-way, connection-based byte streams.
print('socket created')
 
#Bind socket to Host and Port
try:
    s.bind((HOST, PORT))
except socket.error as err:
    print('Bind Failed, Error Code: ' + str(err[0]) + ', Message: ' + err[1])
    sys.exit()
 
print('Socket Bind Success!')
 
#listen(): This method sets up and start TCP listener.
s.listen(10)
print('Socket is now listening')

#Blocking: accept connection
conn, addr = s.accept()

'''
plt.style.use('ggplot')

def live_plotter(x_vec,y1_data,y2_data,line1,line2,identifier='',pause_time=0.1):
    if (line1==[]):
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        #fig = plt.figure(figsize=(13,6))
        fig = plt.figure(figsize=(20,10))
        ax = fig.add_subplot(111)
        
        # create a variable for the line so we can later update it       
        line1, = ax.plot(x_vec,y1_data,'-+', alpha=0.8)
        line2, = ax.plot(x_vec,y2_data,'-o',alpha=0.8)
        
        #update plot label/title and legend keys
        line1.set_label('East Axis')
        line2.set_label('North Axis')
        ax.legend(loc='upper left')
        plt.ylabel('Accel (m/s^2)')
        plt.xlabel('Time (s)')
        plt.title('Acceleration Over Time'.format(identifier))
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_data(x_vec,y1_data)
    line2.set_data(x_vec,y2_data)
    
    # adjust limits if new data goes beyond bounds
    plt.xlim(np.min(x_vec),np.max(x_vec))
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
        
    # adjust limits if new data goes beyond bounds
    if np.min(y2_data)<=line2.axes.get_ylim()[0] or np.max(y2_data)>=line2.axes.get_ylim()[1]:
        plt.ylim([np.min(y2_data)-np.std(y2_data),np.max(y2_data)+np.std(y2_data)])
    
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    lines = [line1, line2]
    # return line so we can update it again in the next iteration
    return lines


#Initialize size of graph    
size = 0
x_vec = []

#y_vecs
y_vecA = []
y_vecB = []

#Each set of data
line1 = []
line2 = []

#Helper method for calculating average of a set of data
def calcAvg(arr):
    #calculates the average of the set
    sum = float(0)
    count = float(0)
    for x in arr:
        sum += x
        count += 1  
    val = sum/count
    return val
    
while True:
    #Pulls current data from the buffer
    buf = conn.recv(4096)
    #converts data from bytes to string
    data = buf.decode("utf-8")
    
    #format of data entry from client: xxxxx:yyyyyy
    #possible data clump due to mis synchronization of client and server: xxxxxx:yyyyyy\nxxxxxx:yyyyyyy\nxxxxxxx:yyyyyy
    #try/exception float conversion error to catch data clumps
    try:
        val = data.split(":")
        
        #If a data clump occurs, these two statements should fail
        #If intended size has not been reached, we append, if it has been reached, we keep the size
        lineA = float(val[0])
        lineB = float(val[1])
        time = float(val[2])
        
        #plots the data sets, since no data clump
        if(size < 100):
            y_vecA.append(lineA)
            y_vecB.append(lineB)
            x_vec.append(time)
            size+=1
        else:
            y_vecA[-1] = lineA  
            y_vecB[-1] = lineB
            x_vec[-1] = time
        
        line = live_plotter(x_vec,y_vecA,y_vecB,line1,line2)
        line1 = line[0] 
        line2 = line[1]
        
        #If we reach our intended size, stay that size
        if(size > 99):
            y_vecA = np.append(y_vecA[1:],0.0)
            y_vecB = np.append(y_vecB[1:],0.0)
            x_vec = np.append(x_vec[1:],0.0)
        
    except ValueError:
        #data clump detected, split data by new line character
        subset = data.split("\n")
        subA = []
        subB = []
        subC = []
        
        #append data to their respective sets
        for x in subset:
            if(len(x) != 0):
                d = x.split(":")
                subA.append(float(d[0]))
                subB.append(float(d[1]))
                subC.append(float(d[2]))
        
        #find average of each set
        avgA = calcAvg(subA)
        avgB = calcAvg(subB)
        avgC = calcAvg(subC)
        
        #plots the data sets, since no data clump
        #If intended size has not been reached, we append, if it has been reached, we keep the size
        if(size < 100):
            y_vecA.append(avgA)
            y_vecB.append(avgB)
            x_vec.append(avgC)
            size+=1
        else:
            y_vecA[-1] = avgA  
            y_vecB[-1] = avgB
            x_vec[-1] = avgC
            
        line = live_plotter(x_vec,y_vecA,y_vecB,line1,line2)
        line1 = line[0] 
        line2 = line[1]
        
        #If we reach our intended size, stay that size
        if(size > 99):
            y_vecA = np.append(y_vecA[1:],0.0)
            y_vecB = np.append(y_vecB[1:],0.0)
            x_vec = np.append(x_vec[1:],0.0)

'''

#Example of plotting two sets of data on SEPARATE subplots
# use ggplot style for more sophisticated visuals
plt.style.use('ggplot')

def live_plotter(x_vec,y1_data,y2_data,line1,line2,identifier='',pause_time=0.1):
    if (line1==[]):
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        
        ax1 = fig.add_subplot(221)
        ax2 = fig.add_subplot(222)
        
        # create a variable for the line so we can later update it       
        line1, = ax1.plot(x_vec,y1_data,'-+',alpha=0.8)
        line2, = ax2.plot(x_vec,y2_data,'-+',alpha=0.8)
        
        #update plot label/title
        line1.axes.set_xlabel('Time')
        line1.axes.set_ylabel('m/s^2')
        line1.axes.title.set_text('Acceleration Over Time')
        
        line2.axes.set_xlabel('Time')
        line2.axes.set_ylabel('m/s')
        line2.axes.title.set_text('Velocity Over Time')
        
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_data(x_vec,y1_data)
    line2.set_data(x_vec,y2_data)
    
    # adjust limits if new data goes beyond bounds
    line1.axes.set_xlim(np.min(x_vec),np.max(x_vec))
    line2.axes.set_xlim(np.min(x_vec),np.max(x_vec))
    
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        line1.axes.set_ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
        
    if np.min(y2_data)<=line2.axes.get_ylim()[0] or np.max(y2_data)>=line2.axes.get_ylim()[1]:
        line2.axes.set_ylim([np.min(y2_data)-np.std(y2_data),np.max(y2_data)+np.std(y2_data)])
    
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    lines = [line1, line2]
    # return line so we can update it again in the next iteration
    return lines

#Initialize size of graph
size = 0
x_vec = []

#y_vecs
y_vecA = []
y_vecB = []

#Each set of data
line1 = []
line2 = []

#Helper method for calculating average of a set of data
def calcAvg(arr):
    #calculates the average of the set
    sum = float(0)
    count = float(0)
    for x in arr:
        sum += x
        count += 1  
    val = sum/count
    return val
    
while True:
    #Pulls current data from the buffer
    buf = conn.recv(4096)
    #converts data from bytes to string
    data = buf.decode("utf-8")
    
    #format of data entry from client: xxxxx:yyyyyy
    #possible data clump due to mis synchronization of client and server: xxxxxx:yyyyyy\nxxxxxx:yyyyyyy\nxxxxxxx:yyyyyy
    #try/exception float conversion error to catch data clumps
    try:
        val = data.split(":")
        
        #If a data clump occurs, these two statements should fail
        lineA = float(val[0])
        lineB = float(val[1])
        time = float(val[2])
        
        if(size < 100):
            y_vecA.append(lineA)
            y_vecB.append(lineB)
            x_vec.append(time)
            size+=1
        else:
            y_vecA[-1] = lineA  
            y_vecB[-1] = lineB
            x_vec[-1] = time
        
        line = live_plotter(x_vec,y_vecA,y_vecB,line1,line2)
        line1 = line[0] 
        line2 = line[1]
        
        if(size > 99):
            y_vecA = np.append(y_vecA[1:],0.0)
            y_vecB = np.append(y_vecB[1:],0.0)
            x_vec = np.append(x_vec[1:],0.0)
        
    except ValueError:
        #data clump detected, split data by new line character
        subset = data.split("\n")
        subA = []
        subB = []
        subC = []
        
        #append data to their respective sets
        for x in subset:
            if(len(x) != 0):
                d = x.split(":")
                subA.append(float(d[0]))
                subB.append(float(d[1]))
                subC.append(float(d[2]))
        
        #find average of each set
        avgA = calcAvg(subA)
        avgB = calcAvg(subB)
        avgC = calcAvg(subC)
        
        if(size < 100):
            y_vecA.append(avgA)
            y_vecB.append(avgB)
            x_vec.append(avgC)
            size+=1
        else:
            y_vecA[-1] = avgA  
            y_vecB[-1] = avgB
            x_vec[-1] = avgC
        
        line = live_plotter(x_vec,y_vecA,y_vecB,line1,line2)
        line1 = line[0] 
        line2 = line[1]
        
        if(size > 99):
            y_vecA = np.append(y_vecA[1:],0.0)
            y_vecB = np.append(y_vecB[1:],0.0)
            x_vec = np.append(x_vec[1:],0.0)
        