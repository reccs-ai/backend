import "./VideoPlayer.css";
import { useRef, useState, useEffect } from "react";

const VideoPlayer = ({ videoUrl }) => {
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  // note, playbackRate is the state we keep track of
  // the actual speed of video is stored in videoRef.current.playbackRate
  const [playbackRate, setPlaybackRate] = useState(1);

  const togglePlay = () => {
    if (videoRef.current.paused) {
      videoRef.current.play();
    } else {
      videoRef.current.pause();
    }
    setIsPlaying(!isPlaying);
  };

  const seekBackward = () => {
    videoRef.current.currentTime -= 5; // 5 seconds
  };

  const seekForward = () => {
    videoRef.current.currentTime += 5;
  };

  const changePlaybackRate = (rate) => {
    videoRef.current.playbackRate = playbackRate; // this line is not necessary but required to remove ESLint build errors
    videoRef.current.playbackRate = rate;
    setPlaybackRate(rate);
  };

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.target.classList.contains("video")) {
        // focusing on video element causes unexpected play/pause behaviour
        // this prevents video element from being in focus with keypress event
        event.preventDefault();
        videoRef.current.blur();
      }
      // play / pause
      if (event.code === "Space") {
        togglePlay();
      }
      // skip backwards
      else if (event.code === "ArrowLeft") {
        seekBackward();
      }
      // skip forwards
      else if (event.code === "ArrowRight") {
        seekForward();
      }
      // speed up
      else if (event.code === "ArrowUp" && videoRef.current.playbackRate < 2) {
        changePlaybackRate(videoRef.current.playbackRate + 0.25);
      }
      // slow down
      else if (
        event.code === "ArrowDown" &&
        videoRef.current.playbackRate > 0.25
      ) {
        changePlaybackRate(videoRef.current.playbackRate - 0.25);
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  });

  return (
    <div>
      <video className="video" ref={videoRef} src={videoUrl} controls />
      {/* Section below is commented out because controls become in focus
      and leads to unexpected control behaviour.
      Also keep in mind that playbackRate state may not be in sync with videoRef.current.playbackRate...
      videoRef.current.playbackRate is a built in var that contains actual speed of video player */}
      {/* <div className="video-controls">
        <label>Video Controls:</label>
        <button onClick={togglePlay}>{isPlaying ? "Pause" : "Play"}</button>
        <button onClick={seekBackward}>Seek Backward</button>
        <button onClick={seekForward}>Seek Forward</button>
      </div>
      <div className="speed-controls">
        <label>Playback Speed:</label>
        <button onClick={() => changePlaybackRate(0.5)}>0.5x</button>
        <button onClick={() => changePlaybackRate(0.75)}>0.75x</button>
        <button onClick={() => changePlaybackRate(1)}>1x</button>
        <button onClick={() => changePlaybackRate(1.25)}>1.25x</button>
      </div> */}
    </div>
  );
};

export default VideoPlayer;
