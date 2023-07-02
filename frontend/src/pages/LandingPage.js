import "./LandingPage.css";
import BuyMeACoffeeButton from "../components/BuyMeACoffeeButton";
import HighlightableText from "../components/HighlightableText";
import landingImage from "../assets/images/landingpage_icon.png";
import { ReactComponent as Logo } from "../assets/images/reccslogo.svg";
import { ReactComponent as InstagramIcon } from "../assets/images/instagram-icon.svg";
import { ReactComponent as TiktokIcon } from "../assets/images/tiktok-icon.svg";

function LandingPage() {
  return (
    <div className="container">
      <header className="header">
        <Logo className="reccs-logo" />
        <BuyMeACoffeeButton />
      </header>
      <div className="main">
        <div className="main-text">
          {/** LHS: text + buttons */}
          <h1 className="headline">
            Transform your <HighlightableText text="dance" /> moves
          </h1>
          <p className="tagline">
            Go from beginner to pro by getting feedback on every move
          </p>
          <div className="cta">
            <a href="https://forms.gle/HYSbdDK7BRuQ1Ris5">
              <button className="cta-button">Get Early Access</button>
            </a>
            <div className="socials">
              <a href="https://www.instagram.com/reccs.ai/">
                <InstagramIcon className="ig-icon" />
              </a>
              <a href="https://www.tiktok.com/@reccs.ai">
                <TiktokIcon className="tiktok-icon" />
              </a>
            </div>
          </div>
        </div>
        <div className="main-image">
          <img src={landingImage} alt="Dancer" className="landing-image" />
        </div>
      </div>
    </div>
  );
}

export default LandingPage;
