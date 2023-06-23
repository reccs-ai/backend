import cv2
import time

from contextlib import contextmanager
from pose import poseDetector

#Which angles will be captured
nodeJoints = [
    [13,11,23], # left shoulder
    [15,13,11], # left elbow
    [14,12,24], # right shoulder
    [16,14,12], # right elbow
    [11,23,25], # left hip
    [23,25,27], # left knee
    [25,27,31], # left ankle
    [12,24,26], # right hip
    [24,26,28], # right knee
    [26,28,32], # right ankle
]

nodeJointList = [
    "nose",                 # 0
    "left eye (inner)",     # 1
    "left eye",             # 2
    "left eye (outer)",     # 3
    "right eye (inner)",    # 4
    "right eye",            # 5
    "right eye (outer)"     # 6
    "left ear",             # 7
    "right ear",            # 8
    "mouth (left)",         # 9
    "mouth (right)",        # 10
    "left shoulder",        # 11
    "right shoulder",       # 12
    "left elbow",           # 13
    "right elbow",          # 14
    "left wrist",           # 15
    "right wrist",          # 16
    "left pinky",           # 17
    "right pinky",          # 18
    "left index",           # 19
    "right index",          # 20
    "left thumb",           # 21
    "right thumb",          # 22
    "left hip",             # 23
    "right hip",            # 24
    "left knee",            # 25
    "right knee",           # 26
    "left ankle",           # 27
    "right ankle",          # 28
    "left heel",            # 29
    "right heel",           # 30
    "left foot index",      # 31
    "right foot index",     # 32
]

ref1 = "videos/practice-omg.mp4"

prevTime = time.time()

detector1 = poseDetector()

cap1 = cv2.VideoCapture(ref1)

instanceAngles1 = [0] * 10
file1 = open("nj-omg-points.txt", "w")

while cap1.isOpened():

    success1, frame1 = cap1.read()

    if not success1:
        print('Cant read the video , Exit!')
        break

    frame1 = cv2.resize(frame1, (1280, 720))
    frame1 = cv2.flip(frame1, 1)
    frame1 = detector1.findPose(frame1, draw=False)
    detector1.findPosition(frame1, draw=False)

    frame1 = detector1.findPose(frame1, draw=False)
    if detector1.results.pose_landmarks != None:
        keypoints = []
        for i, landmark in enumerate(detector1.results.pose_landmarks.landmark):
            x = int(landmark.x * frame1.shape[1])
            y = int(landmark.y * frame1.shape[0])
            cv2.circle(frame1, (x, y), 5, (255, 0, 0), cv2.FILLED)
            keypoints.append((x, y))
        
        strOut = str(keypoints).strip('[]') + "\n"
        file1.write(strOut)
    else:
        file1.write("None\n")

    cv2.imshow('Instructor' , frame1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()
file1.close()
cv2.destroyAllWindows()