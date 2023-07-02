import { useState, useEffect, useRef } from "react";
import "./HighlightableText.css";

const HighlightableText = ({ text }) => {
  const textRef = useRef(null);
  const [blueHighlightStyle, setBlueHighlightStyle] = useState(null);
  const [pinkHighlightStyle, setPinkHighlightStyle] = useState(null);

  // resizes highlight based on screensize
  const handleResize = () => {
    const textElement = textRef.current;
    const textRect = textElement.getBoundingClientRect();
    // blue highlight
    const blueHighlightStyle = {
      top: `${textRect.width * 0.23}px`,
      left: `-1rem`,
      width: `${textRect.width * 1.1}px`,
      height: `${textRect.height * 0.4}px`,
      backgroundColor: "rgba(90, 255, 245, 0.3)",
      position: "absolute",
    };
    setBlueHighlightStyle(blueHighlightStyle);
    // pink highlight
    const pinkHighlightStyle = {
      top: `${textRect.width * 0.31}px`,
      left: `0.2rem`,
      width: `${textRect.width * 1.08}px`,
      height: `${textRect.height * 0.3}px`,
      backgroundColor: "rgba(255, 0, 199, 0.3)",
      position: "absolute",
    };
    setPinkHighlightStyle(pinkHighlightStyle);
  };

  useEffect(() => {
    window.addEventListener("resize", handleResize);
    const delay = setTimeout(handleResize, 100); // Delay the calculation to ensure proper highlighting
    return () => clearTimeout(delay);
  }, []);

  return (
    <span
      ref={textRef}
      id="highlightable-text"
      style={{ position: "relative" }}
    >
      <span className="text-class">{text}</span>
      {blueHighlightStyle && <span style={blueHighlightStyle} />}
      {pinkHighlightStyle && <span style={pinkHighlightStyle} />}
    </span>
  );
};

export default HighlightableText;
