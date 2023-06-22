import cv2
from mediapipe import solutions
import time
import math

class poseDetector():
    def __init__(self, mode=False):
        self.mode = mode
        self.mpDraw = solutions.drawing_utils
        self.mpPose = solutions.pose
        self.pose = self.mpPose.Pose(self.mode, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Finds pose of person
    def findPose(self, img, draw=True):
        # Converts one color space to another
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
    
    # Superimposes the nodes of video 1 on video 2
    def superimpose(self, img, bg, node_color=(200, 200, 0), node_size=5, connector_color=(170, 150, 0), connector_thickness=5):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            self.mpDraw.draw_landmarks(bg, self.results.pose_landmarks,
                                       self.mpPose.POSE_CONNECTIONS,
                                       self.mpDraw.DrawingSpec(color=node_color, thickness=2, circle_radius=node_size),
                                       self.mpDraw.DrawingSpec(color=connector_color, thickness=5, circle_radius=connector_thickness))
        return img
    
    # Finds position of person
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, _ = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    # Finds angle between three different nodes
    def findAngle(self, img, p1, p2, p3, draw=True, addNumbers=True):

        # Get the landmarks
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]

        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))

        if angle < 0:
            angle += 360
            
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
        
        # Add degrees
        if addNumbers:
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (100, 100, 255), 2)
            cv2.putText(img, str(p1), (x2 + 30, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (100, 255, 100), 2)
        return angle


def main():
    vid = cv2.VideoCapture(0)
    prevTime = 0
    detector = poseDetector()
    while True:
        _, img = vid.read() 
        img = detector.findPose(img)

        # lmList = detector.findPosition(img, draw=False)

        # if len(lmList) != 0:
        #     print(lmList[14])
        #     cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

        curTime = time.time()
        fps = 1 / (curTime - prevTime)
        prevTime = curTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("frame", img)

        # Amount of time the window is displayed in ms or until q key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()