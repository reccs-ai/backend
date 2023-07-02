import axios from 'axios';
import VideoNotes from "../components/VideoNotes";
import videoFile from "../assets/videos/dance1.mp4";

const notes = {
  "00:05": "Make arms bigger",
  "00:11": "Bend upper body to be lower",
  "00:15": "Jump higher",
  "00:19": "Keep arms closer to body",
};

const StudentLearningPage = () => {
  let x = axios.get("http://localhost:5000/hello").then(function (response) {console.log(response.data)})
  return (
    <div className="classroom-container">
      <VideoNotes videoUrl={videoFile} notes={notes} />
    </div>
  );
};

export default StudentLearningPage;
