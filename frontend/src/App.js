import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import StudentLearningPage from "./pages/StudentLearningPage";
import FeedbackPage from "./pages/FeedbackPage";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<LandingPage />} />
        <Route exact path="/demo" element={<StudentLearningPage />} />
        <Route exact path="/feedback" element={<FeedbackPage />} />
        <Route exact path="/*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

export default App;
