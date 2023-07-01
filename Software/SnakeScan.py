# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 13:20:14 2023

@author: luke_
"""

import matplotlib.pyplot as plt
import numpy as np
import serial
from picamera import PiCamera
from functions import *


if __name__ == "__main__":
    folder = "/home/pi/Desktop/Ender_CamMotion/MP12.06.23/B1.2T24C3/"
    # open port and camera
    # open serial port (motion via gcode)
    ser = serial.Serial('/dev/ttyUSB0', baudrate=115200)
    xBase = "G1X"
    yBase = "Y"
    endTerm = "\n"
    speed = 18000   #max_speed
#     home = "G28" + "F" + str(speed) + "\n"
#     home = home.encode('utf-8')
#     ser.write(home)
    x_mid = 0
    y_mid = 0
    startPos = xBase + str(x_mid) + yBase + str(y_mid) + "F" + str(speed) + endTerm
    startPos = startPos.encode('utf-8')
    ser.write(startPos) # go to half max
   # time.sleep(16)
    # open camera (image acquisition)
    camera = PiCamera()

def snake (x_win, y_win, width):
    a = [] #a is list of all x pos - empty list
    b = [] #b is list of all y pos
    x = 1
    y = 1 # start point of bed
#     a.append(x) #take a and stick x into it, so 0 is first number in list
#     b.append(y)
    
    
    for j in range (y_win - 1):
        
        if j == 0 :
            
            for i in range(x_win): #increment x step
                
                if i % x_win != 0:
                    dx = 6.4
                    dy = 0
                    
                elif i % x_win == 0:
                    dx = 0
                    dy = 0
                    
                x = x + dx
                y = y + dy
                
                a.append(x) #take a and stick x into it, so 0 is first number in list
                b.append(y)  
            
        
        if j % 2 != 0:
            
            for i in range(x_win):
                
                if i % x_win != 0:
                    dx = 6.4
                    dy = 0
                    
                elif i % x_win == 0:
                    dx = 0
                    dy = 6.4
                    
                x = x + dx
                y = y + dy
                
                a.append(x) #take a and stick x into it, so 0 is first number in list
                b.append(y)      
                        
        elif j % 2 ==0:
            
            for i in range(x_win):
            
                if i % x_win != 0:
                    dx = -6.4
                    dy = 0
                    
                elif i % x_win == 0:
                    dx = 0
                    dy = 6.4
                
                x = x + dx
                y = y + dy
                a.append(x) #take a and stick x into it, so 0 is first number in list
                b.append(y)
             
    spread_x = np.max(np.abs(a)) #go to list and find max a
    spread_y = np.max(np.abs(b))
    
    x_vals = np.array(a)*width/spread_x #take our list and make it an array - can be recognised elsewhere in code as numbers
    y_vals = np.array(b)*width/spread_y
    x_vals = np.array(a)
    y_vals = np.array(b)
    
    print (x)
    print (y)
    
    return x_vals, y_vals 

x,y = snake(23, 23, 147.2) # start from bottom left corner   

plt.plot(x, y, marker='x')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Snake Scan')
plt.grid(True)
plt.show()

    # wait until key is pressed
tune = "M300 S440 P200" + endTerm
ser.write(tune.encode('utf-8'))
pause = "M25" + endTerm
ser.write(pause.encode('utf-8'))
print('Place sample')
input("Press the Enter key to proceed")

resume = "M108" + endTerm
ser.write(resume.encode('utf-8'))

    # take images + on-the-fly image processing
   # camera.start_preview(resolution=(640, 480))
for i in range(len(x)):
    #camera.resolution = (640, 480)
    xPos = x_mid + x[i]
    yPos = x_mid + y[i]
    Mot = xBase + str(xPos) + yBase + str(yPos) + "F" + str(speed) + endTerm
    Mot = Mot.encode('utf-8')
    ser.write(Mot)
    time.sleep(0.5)
    camera.capture("%s_%s.bmp" % (folder, i))
    time.sleep(0.5)