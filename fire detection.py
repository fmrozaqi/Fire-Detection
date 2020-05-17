import cv2
import numpy as np
import math
import sys

# Video Capture
cap = cv2.VideoCapture("tes4.mp4")

# Get the resolution
w, h = int(cap.get(3)), int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30.0, (w,h))

# Size of the green square
x = 5 

# Count the positive value of pixels every square 
count = np.zeros(w//x + 1)

# Threshold Red value
tRed = 170

# Threshold Positive value
tPositive = 10

totalFPS = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
FPSnow = 1
print("PROCESS STARTING...")
while(True):
    #Get Frame and HSV value, Duplicate frame to get the difference between native image and new image
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame2 = frame.copy()

    for i in range(h):
        for j in range(w):

            # Get value of pixel
            blue = int(frame[i][j][0])
            green = int(frame[i][j][1])            
            red = int(frame[i][j][2])
            saturation = int(hsv[i][j][1])

            # initialize y1 and y2
            y1 = (100 - 0.3922*frame[i][j][0]) / 100 * 255
            y2 = (-2.0147 + 90.59435 * math.exp(-blue/77.6027)) / 100 * 255 
            
            if red >= green and green >= blue :                          # Red >= Green >= Blue
                if red > tRed :                                         # red > tRed
                    if  y2 < saturation and y1 > saturation :           # y1 > saturation > y2
                        count[j//x] += 1                                # count positive value every square x*x

            if (i+1)%x==0 and (j+1)%x==0:                               # every square x*x
                if (count[j//x] >= tPositive):                          # positive value > tPositive 
                    cv2.rectangle(frame,(j-x,i-x),(j,i),(0,255,0),1)    # make green square
                count[j//x] = 0                                         # reset value 
   
    # Display the resulting frame    
    # cv2.imshow('frame',frame)
    # cv2.imshow('frame2',frame2)

    # Write the frame into the file 'output.avi'
    out.write(frame)

    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    sys.stdout.write('\rloading ' + str(FPSnow) + " /" + str(totalFPS))
    FPSnow += 1

print("FINISH")
# When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv2.destroyAllWindows()
