import cv2 as cv
import handTrackingModule as htm
import numpy as np
import time
from collections import deque

capture= cv.VideoCapture(0)
new_frame=0
prev_frame=0
detector=htm.HandDetector()

# These indexes will be used to mark the points in particular arrays of specific colour
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

# Giving different arrays to handle colour points of different colour
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]  
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

#The kernel to be used for dilation purpose 
kernel = np.ones((5,5),np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

canvas = np.zeros((471,636,3)) + 255
canvas = cv.rectangle(canvas, (40,1), (140,65), (0,0,0), 2)
canvas = cv.rectangle(canvas, (160,1), (255,65), colors[0], -1)
canvas = cv.rectangle(canvas, (275,1), (370,65), colors[1], -1)
canvas = cv.rectangle(canvas, (390,1), (485,65), colors[2], -1)
canvas = cv.rectangle(canvas, (505,1), (600,65), colors[3], -1)

cv.putText(canvas, "CLEAR", (49, 33), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0, 0, 0), 1, cv.LINE_AA)
cv.putText(canvas, "BLUE", (185, 33), cv.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
cv.putText(canvas, "GREEN", (298, 33), cv.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
cv.putText(canvas, "RED", (420, 33), cv.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
cv.putText(canvas, "YELLOW", (520, 33), cv.FONT_HERSHEY_TRIPLEX, 0.5, (150,150,150), 1, cv.LINE_AA)
cv.namedWindow('Paint', cv.WINDOW_AUTOSIZE)


while True:
    success, frame= capture.read()
    frame=cv.flip(frame,1)

    # Adding the colour buttons to the live frame for colour access
    frame = cv.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
    frame = cv.rectangle(frame, (160,1), (255,65), colors[0], -1)
    frame = cv.rectangle(frame, (275,1), (370,65), colors[1], -1)
    frame = cv.rectangle(frame, (390,1), (485,65), colors[2], -1)
    frame = cv.rectangle(frame, (505,1), (600,65), colors[3], -1)
    cv.putText(frame, "CLEAR ALL", (49, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, "BLUE", (185, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, "GREEN", (298, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, "RED", (420, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, "YELLOW", (520, 33), cv.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv.LINE_AA)

    frame=detector.findHand(frame, draw=True)
    lmlist=detector.findPosition(frame, draw=False)

    if len(lmlist)>0:
        x1,y1=lmlist[8][1],lmlist[8][2] 
        x2,y2=lmlist[12][1],lmlist[12][2] 

        cv.circle(frame,(x1,y1),15,(130,100,195),thickness=-1)
        cv.circle(frame,(x2,y2),15,(130,100,195),thickness=-1)

        
        center=[int(x1),int(y1)]



        # Now checking if the user wants to click on any button above the screen 
        if center[1] <= 65:
            if 40 <= center[0] <= 140: # Clear Button
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]

                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0

                canvas[67:,:,:] = 255
            elif 160 <= center[0] <= 255:
                    colorIndex = 0 # Blue
            elif 275 <= center[0] <= 370:
                    colorIndex = 1 # Green
            elif 390 <= center[0] <= 485:
                    colorIndex = 2 # Red
            elif 505 <= center[0] <= 600:
                    colorIndex = 3 # Yellow
        else :
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1: 
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)
    # Append the next deques when nothing is detected to avois messing up
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    # Draw lines of all the colors on the canvas and frame 
    if len(lmlist)>0:
        points = [bpoints, gpoints, rpoints, ypoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                    cv.line(canvas, points[i][j][k - 1], points[i][j][k], colors[i], 2)   


    new_frame=time.time()
    fps=1/(new_frame-prev_frame)
    prev_frame=new_frame

    cv.putText(frame,f'FPS: {int(fps)}', (30,470), cv.FONT_HERSHEY_TRIPLEX, 1, (100,255,250), thickness=1)

       # Show all the windows
    cv.imshow("Tracking", frame)
    cv.imshow("Paint", canvas)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break

# Release the camera and all resources
capture.release()
cv.destroyAllWindows()
