import math
import cv2
from mediapipe import solutions

jointNodeList = [
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

jointNodeMap = [
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

class poseDetector():

    # Instaniating variables
    def __init__(self, mode=False):
        self.mode = mode
        self.mpDraw = solutions.drawing_utils
        self.mpPose = solutions.pose
        self.pose = self.mpPose.Pose(self.mode)
        
    
    # Finds position of person
    def findPosition(self, img, draw=True):
        self.lmList = []
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        h, w, _ = img.shape

        if self.results.pose_landmarks:
            for i, lm in enumerate(self.results.pose_landmarks.landmark):
                x, y = int(lm.x * w), int(lm.y * h)
                self.lmList.append((x, y))
                if draw:
                    cv2.circle(img, (x, y), 5, (255, 0, 0), cv2.FILLED)

        return self.lmList


def processVideo(filename, lm_filename):
    # Processes the video into a file of landmarks (x, y) for a particular frame
    cap = cv2.VideoCapture(filename)
    lm_file = open(lm_filename, "w")
    detector = poseDetector()
    all_landmarks_list = []
    
    while cap.isOpened():
        # Read the camera frame
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # find landmark locations
        landmark_list = detector.findPosition(frame)

        if landmark_list:
            landmark_str = str(landmark_list).strip('[]') + "\n"
            lm_file.write(landmark_str)
        else:
            lm_file.write("None\n")

        all_landmarks_list.append(landmark_list)

    cap.release()
    lm_file.close()


def calcAngle(landmark_list, p1, p2, p3):

    # Get the landmarks
    x1, y1 = landmark_list[p1]
    x2, y2 = landmark_list[p2]
    x3, y3 = landmark_list[p3]

    # Calculate the Acute Angle
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    angle = abs(angle)
    if angle > 180:
        angle = 360 - angle
        
    return angle


def createAngleList(lm_filename):
    global jointNodeList

    lm_file = open(lm_filename, "r")
    all_landmark_list = lm_file.read().splitlines()

    all_angle_list = []

    # for each frame: 
    for i in range(len(all_landmark_list)):
        landmark_list = [tuple(int(v) for v in a.strip("()").split(", ")) for a in all_landmark_list[i].split('), (')]
        angle_frame_list = []

        # for each joint node in the frame:
        for j in range(len(jointNodeList)):
            n1, n2, n3 = jointNodeList[j][0], jointNodeList[j][1], jointNodeList[j][2]
            angle = calcAngle(landmark_list, n1, n2, n3)
            angle_frame_list.append(round(angle, 3))

        all_angle_list.append(angle_frame_list)

    return all_angle_list


def showVideo(video_filename, lm_filename):

    all_angle_list = createAngleList(lm_filename)
    
    cap = cv2.VideoCapture(video_filename)

    lm_file = open(lm_filename, "r")
    all_landmarks_list = lm_file.read().splitlines()

    count = 0
    while cap.isOpened() and count < len(all_landmarks_list):

        success, frame = cap.read()

        if not success:
            print('Cant read the video , Exit!')
            break

        frame = cv2.flip(frame, 1)

        angle_list = all_angle_list[count]
        if all_landmarks_list[count] != "None":
            landmarks_list = [tuple(int(v) for v in a.strip("()").split(", ")) for a in all_landmarks_list[count].split('), (')]

            for i in range(len(jointNodeList)):
                p1, p2, p3 = jointNodeList[i][0], jointNodeList[i][1], jointNodeList[i][2]
                x1, y1 = landmarks_list[p1]
                x2, y2 = landmarks_list[p2]
                x3, y3 = landmarks_list[p3]
                cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 3)
                cv2.line(frame, (x3, y3), (x2, y2), (255, 255, 255), 3)
                cv2.circle(frame, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(frame, (x1, y1), 15, (0, 0, 255), 2)
                cv2.circle(frame, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(frame, (x2, y2), 15, (0, 0, 255), 2)
                cv2.circle(frame, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
                cv2.circle(frame, (x3, y3), 15, (0, 0, 255), 2)
            
            
                cv2.putText(frame, str(int(angle_list[i])), (x2 - 50, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (100, 100, 255), 2)
                cv2.putText(frame, str(p1), (x2 + 30, y2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, (100, 255, 100), 2)

            x11, y11 = landmarks_list[11]
            x12, y12 = landmarks_list[12]
            x23, y23 = landmarks_list[23]
            x24, y24 = landmarks_list[24]

            cv2.line(frame, (x11, y11), (x12, y12), (255, 255, 255), 3)
            cv2.line(frame, (x23, y23), (x24, y24), (255, 255, 255), 3)
            
        count += 1

        cv2.imshow('Instructor' , frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    lm_file.close()
    cv2.destroyAllWindows()


def skeletonVideo(video_filename, output_filename):
    
    cap = cv2.VideoCapture(video_filename)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    
    size = (frame_width, frame_height)
    result = cv2.VideoWriter(output_filename, cv2.VideoWriter_fourcc(*'MP4V'), 10, size)
    detector = poseDetector()
    
    while cap.isOpened():
        # Read the camera frame
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # find landmark locations
        detector.findPosition(frame)

        result.write(frame)
        cv2.imshow('frame',frame)
        
    result.release()
    cap.release()
    cv2.destroyAllWindows()


def main():
    # showVideo("videos/RobotDance.mov", "RobotDance.txt")
    skeletonVideo("videos/RobotDance.mov", "videos/res.mp4")


if __name__ == "__main__":
    main()