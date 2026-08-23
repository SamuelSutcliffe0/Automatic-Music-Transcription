import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./screens/home";
import Login from "./screens/login";
import Signup from "./screens/signup";
import Welcome from "./screens/welcome";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/welcome" element={<Welcome />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;