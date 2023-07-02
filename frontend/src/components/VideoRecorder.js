import React, { useRef } from "react";

const VideoRecorder = () => {
  const videoRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);

  const handleStartRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.addEventListener(
        "dataavailable",
        handleDataAvailable
      );
      mediaRecorderRef.current.start();
    } catch (error) {
      console.error("Error accessing the camera:", error);
    }
  };

  const handleStopRecording = () => {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state === "recording"
    ) {
      mediaRecorderRef.current.stop();
    }
  };

  const handleDataAvailable = (event) => {
    if (event.data.size > 0) {
      chunksRef.current.push(event.data);
    }
  };

  const handleSaveVideo = () => {
    const blob = new Blob(chunksRef.current, { type: "video/webm" });
    const url = URL.createObjectURL(blob);

    // Create a download link for the video
    const link = document.createElement("a");
    link.href = url;
    link.download = "mirror-video.webm";
    link.click();

    // Clean up
    chunksRef.current = [];
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <video ref={videoRef} autoPlay muted />
      {/* TODO: Showcase camera recording status, allow the user to control camera on/off, but default to camera on */}
      {/* <label>Camera Status: {mediaRecorderRef.current.state}</label> */}
      <div>
        <button onClick={handleStartRecording}>Start Recording</button>
        <button onClick={handleStopRecording}>Stop Recording</button>
        <button onClick={handleSaveVideo}>Save Video</button>
      </div>
    </div>
  );
};

export default VideoRecorder;
