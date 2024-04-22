import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import "./App.css";
import Navbar from "./components/Navbar";
import { Home } from "./components/Home";
import SignUp from "./components/SignUp";
import Login from "./components/Login";
import LearnerCourses from "./components/LearnerCourses";

function App() {
  return (
    <div className="App">
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />

          <Route path="/signup" element={<SignUp />} />

          <Route path="/login" element={<Login />} />

          <Route path="/courses" element={<LearnerCourses />} />

        </Routes>
      </Router>
    </div>
  );
}

export default App;
