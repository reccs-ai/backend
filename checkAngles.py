import cv2
import numpy as np
# from time import time
import mediapipe as mp
import pandas as pd
import os
import pose as pm
from contextlib import contextmanager
import sys, os

#to suppress output
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout


#Which angles will be captured
nodeJoints = [
    [13,11,23], 
    [15,13,11],
    [14,12,24],
    [16,14,12],
    [11,23,25],
    [23,25,27],
    [25,27,31],
    [12,24,26],
    [24,26,28],
    [26,28,32],
]

#Getting video input from user's webcam
cap = cv2.VideoCapture(0)

#stores instance angles
instance_angles = [0] * 10

#Instantiating pose detector
detector = pm.poseDetector()

while True:
    
    # Reading camera input
    success, frame = cap.read()

    if not success:
        continue
    
    # Resizing image
    img = cv2.resize(frame, (1280, 720))
    
    #flip image horizontally to mirror user
    img = cv2.flip(img, 1)
    
    with suppress_stdout():
    #Shows the user the nodes and finds their pose
        img = detector.findPose(img, draw=False)
        lmList = detector.findPosition(img, draw=False)

    # Shows the full body angles
    if len(lmList) != 0:
        for i in range(len(nodeJoints)):
            instance_angles[i] = (detector.findAngle(img, nodeJoints[i][0], nodeJoints[i][1], nodeJoints[i][2], True, True))
        x11, y11 = detector.lmList[11][1:]
        x12, y12 = detector.lmList[12][1:]
        x23, y23 = detector.lmList[23][1:]
        x24, y24 = detector.lmList[24][1:]

        cv2.line(img, (x11, y11), (x12, y12), (255, 255, 255), 3)
        cv2.line(img, (x23, y23), (x24, y24), (255, 255, 255), 3)
        
    cv2.imshow("Image", img)
    # Amount of time the window is displayed in ms or until q key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break