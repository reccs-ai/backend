from pose import poseDetector
import time
import math
from flask import Flask,render_template,Response
import cv2

app=Flask(__name__)


def generate_frames():
    camera = cv2.VideoCapture(0)
    prevTime = 0
    # create pose detector to paint skeleton
    detector = poseDetector()
    while True:
        # read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            # flip the frame horizontally
            frame = cv2.flip(frame, 1)
            # add skeleton on person
            frame = detector.findPose(frame)
            curTime = time.time()
            fps = 1 / (curTime - prevTime)
            prevTime = curTime
            cv2.putText(frame, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=False)

