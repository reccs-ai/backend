import React, { useState, useRef } from "react";

const VideoComponent = ({ videoUrl, notes }) => {
  const [editedNotes, setEditedNotes] = useState(notes);
  const videoRef = useRef(null);

  const handleNoteChange = (timestamp, event) => {
    const updatedNotes = { ...editedNotes };
    updatedNotes[timestamp] = event.target.value;
    setEditedNotes(updatedNotes);
  };

  const handleTimestampClick = (timestamp) => {
    const timeParts = timestamp.split(":");
    const minutes = parseInt(timeParts[0]);
    const seconds = parseInt(timeParts[1]);
    const timeInSeconds = minutes * 60 + seconds;
    videoRef.current.currentTime = timeInSeconds;
  };

  return (
    <div>
      <video ref={videoRef} src={videoUrl} controls />
      <ul>
        {Object.entries(editedNotes).map(([timestamp, note]) => (
          <li key={timestamp}>
            <span onClick={() => handleTimestampClick(timestamp)}>
              {timestamp}:
            </span>
            <input
              type="text"
              value={note}
              onChange={(event) => handleNoteChange(timestamp, event)}
            />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VideoComponent;
