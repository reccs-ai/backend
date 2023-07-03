from flask import Flask, render_template, Response
from flask_cors import CORS
import cv2

from compare import compareVideos
from pose import poseDetector

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

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

    # Create pose detector to draw the skeleton
    detector = poseDetector()
    while cap.isOpened():
        # Read the camera frame
        ret, frame = cap.read()
        if not ret:
            break
        
        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Add skeleton on person
        detector.findPosition(frame)

        # Calculate the frame rate
        # curTime = time.time()
        # fps = 1 / (curTime - prevTime)
        # prevTime = curTime
        # cv2.putText(frame, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # Save the frame to the video file
        out.write(frame)

        # Save as jpg to send as a stream
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()
    out.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return "hello"

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/save_video', methods=['POST'])
def save_video():
    global cap, out

    # Release resources
    cap.release()
    out.release()

    return render_template('compare.html')

@app.route('/compare', methods=['POST'])
def compare():
    
    ref1 = "landmarks/RobotDance.txt"
    ref2 = "landmarks/StudentDance.txt"
    
    danceScore, flaggedTimeStamps, percentErrorList = compareVideos(ref1, ref2)

    return "Dance Score: " + str(danceScore)

if __name__=="__main__":
    app.run(debug=False)

