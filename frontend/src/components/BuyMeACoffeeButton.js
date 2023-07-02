import "./BuyMeACoffeeButton.css";
import { useState, useEffect } from "react";
import { ReactComponent as Coffee } from "../assets/images/coffee.svg";

const BuyMeACoffeeButton = () => {
  // manages button text based on screen size
  const [buttonText, setButtonText] = useState("Buy us a coffee");
  useEffect(() => {
    // determines the initial text for button depending on screen size
    if (window.innerWidth < 768) {
      setButtonText("Buy us a ");
    } else {
      setButtonText("Buy us a coffee ");
    }
    // determins the text when screen is resized
    const handleResize = () => {
      if (window.innerWidth < 768) {
        setButtonText("Buy us a");
      } else {
        setButtonText("Buy us a coffee");
      }
    };
    window.addEventListener("resize", handleResize);
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return (
    <a href="https://www.buymeacoffee.com/reccs">
      <button className="support-button">
        {buttonText} {`\u00A0`} <Coffee className="coffee-icon" />
      </button>
    </a>
  );
};

export default BuyMeACoffeeButton;
