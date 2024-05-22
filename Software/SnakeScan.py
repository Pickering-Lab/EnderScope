import matplotlib.pyplot as plt
import numpy as np
import serial
from picamera import PiCamera
import time


if __name__ == "__main__":
    folder = "/home/pi/" #Replace this with folder you would like your images saved in
    #Opens serial port
    ser = serial.Serial('/dev/ttyUSB0', baudrate=115200)
    xBase = "G1X"
    yBase = "Y"
    endTerm = "\n"
    speed = 18000   #max_speed
##     Uncoment to home printer at beginning of script - ***WARNING*** You must make sure objective lens will not crash in to bed before homing. Attach limit switch extender or remove optics module during homing.
#     home = "G28" + "F" + str(speed) + "\n"
#     home = home.encode('utf-8')
#     ser.write(home)
    x_mid = 0
    y_mid = 0
    startPos = xBase + str(x_mid) + yBase + str(y_mid) + "F" + str(speed) + endTerm
    startPos = startPos.encode('utf-8')
    ser.write(startPos) # go to half max
    # open camera (image acquisition)
    camera = PiCamera()

def snake(x_win, y_win, x_step, y_step):
    a = []  # List of X positions
    b = []  # List of Y positions
    x = 0
    y = 0  # Start point at the bottom left corner
    
    for j in range (y_win - 1):
    
        if j == 0 :
            
            for i in range(x_win): #increment x step
                
                if i % x_win != 0:
                    dx = x_step
                    dy = 0
                    
                elif i % x_win == 0:
                    dx = 0
                    dy = 0
                    
                x = x + dx
                y = y + dy
                
                a.append(x) #take list a and stick x into it, so 0 is first number in list
                b.append(y) #take list b and stick y into it, so 0 is first number in list 
            
        
        if j % 2 != 0:
            
            for i in range(x_win):
                
                if i % x_win != 0:
                    dx = x_step
                    dy = 0
                    
                elif i % x_win == 0:
                    dx = 0
                    dy = y_step
                    
                x = x + dx
                y = y + dy
                
                a.append(x) 
                b.append(y)      
                        
        elif j % 2 ==0:
            
            for i in range(x_win):
            
                if i % x_win != 0:
                    dx = -x_step
                    dy = 0
                    
                elif i % x_win == 0:
                    dx = 0
                    dy = y_step
                
                x = x + dx
                y = y + dy
                
                # Round the x-value to 2 decimal places
                x = round(x, 2)
                
                a.append(x) 
                b.append(y)
                
    x_vals = np.array(a)
    y_vals = np.array(b)
    print (x_vals)
    print (y_vals)
    return a, b

x_win = 3  # Number of steps in the x direction
y_win = 3 # Number of steps in the y direction
x_step = 5  # Step size in the x direction
y_step = 5  # Step size in the y direction
x_mm = x_win*x_step # to calculate area scan will cover in mm
y_mm = y_win*y_step


x, y = snake(x_win, y_win, x_step, y_step)


tune = "M300 S440 P200" + endTerm 
ser.write(tune.encode('utf-8')) # play tune to signal start of scan
pause = "M18" + endTerm # disable stepper - allows user to position optics module in bottom left corner of sample
ser.write(pause.encode('utf-8'))
camera.start_preview(fullscreen=False, window=(100, 100, 640, 480))
print('Steppers have been disabled')
print('Ensure sample is in focus. Then move optics module to bottom left corner of sample')
input("Press the Enter key to proceed")
camera.stop_preview()
resume = "M108" + endTerm
ser.write(resume.encode('utf-8'))

print('This is the path of the snake scan. Close graph to proceed.')
plt.plot(x, y, marker = 'x') # plots path of scan
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Snake Scan')
plt.grid(True)
plt.show()


print(f"This will now start a snake scan, scanning over an area {x_mm} x {y_mm} mm starting from the bottom left corner of the sample, going right and up")
input("Press the Enter key to proceed")
resume = "M108" + endTerm
ser.write(resume.encode('utf-8'))

camera.start_preview(resolution=(640, 480))
for i, (x_val, y_val) in enumerate(zip(x, y), start=1):
        # Move the printer here (adjust the timing as needed)
    xPos = x_mid + x_val
    yPos = y_mid + y_val
    Mot = xBase + str(xPos) + yBase + str(yPos) + "F" + str(speed) + endTerm
    Mot = Mot.encode('utf-8')
    ser.write(Mot)
    time.sleep(1)
    # Use string formatting to create the file name with leading zeros
    num_digits = len(str(len(x)))  # Determine the number of digits needed
    file_name = f"{folder}_{i:0{num_digits}d}.bmp"
    camera.exposure_mode = 'off'
    camera.awb_mode = 'off'
    camera.resolution = (1014, 760)
    # Configure white balance and exposure settings for each image capture
    camera.awb_gains = (1, 1)  # R and B gains, both set to 1.0 for neutral white balance
    camera.shutter_speed = 8000 # exposure setting - adjust as needed particularly for fluorescence imaging
    
    # Capture the image with the constructed file name
    camera.capture(file_name)
    time.sleep(1)
# Close the camera preview when the scan is finished
camera.stop_preview()






