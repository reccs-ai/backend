from pose import poseDetector
from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

cap = None
out = None 

def generate_frames():
    global cap, out

    # Open the video file or capture from a camera
    cap = cv2.VideoCapture(0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    # prevTime = 0

    # create pose detector to paint skeleton
    # detector = poseDetector()
    while cap.isOpened():
        # read the camera frame
        ret, frame = cap.read()
        if not ret:
            break
        
        # flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Save the frame to the video file
        out.write(frame)

        # add skeleton on person
        # frame = detector.findPose(frame)
        # curTime = time.time()
        # fps = 1 / (curTime - prevTime)
        # prevTime = curTime
        # cv2.putText(frame, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()
    out.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/save_video', methods=['POST'])
def save_video():
    global cap, out

    # Release resources
    cap.release()
    out.release()

    return 'Video saved successfully!'

if __name__=="__main__":
    app.run(debug=False)

