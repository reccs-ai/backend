import math
import cv2
from mediapipe import solutions


class poseDetector():

    # Instaniating variables
    def __init__(self, mode=False):
        self.mode = mode
        self.mpDraw = solutions.drawing_utils
        self.mpPose = solutions.pose
        self.pose = self.mpPose.Pose(self.mode)

    # Finds pose of person
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
    
    # Finds position of person
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, _ = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList
    
    # Finds angle between three different nodes
    def findAngle(self, img, p1, p2, p3, draw=True):

        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))

        if angle < 0:
            angle = angle + 360

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle


def main(fileAddress, showVideo, draw):
    cap = cv2.VideoCapture(fileAddress)

    detector = poseDetector()

    absList = []

    while True:

        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        img = detector.findPose(img, draw)
        lmList = detector.findPosition(img, draw)

        absList.append(lmList)

        # print coordinates
        # for i in range(len(lmList)):
        #     print(lmList[i])

        if showVideo:
            img = cv2.flip(img, 1)
            cv2.putText(img, "Dance Pose Analysis:", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    return absList

def calcAngle(f, absList, n1, n2, n3):
    # Get the landmarks
    y3 = absList[f][n3][2]
    y2 = absList[f][n2][2]
    y1 = absList[f][n1][2]

    x3 = absList[f][n3][1]
    x2 = absList[f][n2][1]
    x1 = absList[f][n1][1]

    # Calculate the angle
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))

    if angle < 0:
        angle = abs(angle)

    return angle


def createAngleList(absList):
    jointNodes = [[13, 11, 23], [15, 13, 11], [14, 12, 24], [16, 14, 12], [11, 23, 25], [23, 25, 27], [25, 27, 31],
                  [12, 24, 26], [24, 26, 28], [24, 26, 28], [26, 28, 32]]

    angleList = []

    for i in range(len(absList)):

        subList = []

        # for each frame: 
        for j in range(10):
            a, b, c = jointNodes[j][0], jointNodes[j][1], jointNodes[j][2]
            angle = calcAngle(i, absList, a, b, c)
            subList.append(round(angle, 3))

        angleList.append(subList)

    return angleList


def getAngleList(fileAddress, showVideo, draw):
    absList = main(fileAddress, showVideo, draw)
    # print(absList)
    return createAngleList(absList)

