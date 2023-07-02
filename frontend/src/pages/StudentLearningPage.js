import "./StudentLearningPage.css";
import VideoPlayer from "../components/VideoPlayer";
import VideoRecorder from "../components/VideoRecorder";
// import FlaskCamera from "../components/FlaskCamera";
import videoFile from "../assets/videos/dance1.mp4";

const StudentLearningPage = () => {
  return (
    <div className="classroom-container">
      <div className="instructor">
        Instructor Video:
        <VideoPlayer videoUrl={videoFile} />
      </div>
      <div className="student">
        Student Video:
        <VideoRecorder />
      </div>
    </div>
  );
};

export default StudentLearningPage;
