import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./screens/home";
import Login from "./screens/login";
import Signup from "./screens/signup";
import Welcome from "./screens/welcome";
import About from "./screens/about";
import Tabs from "./screens/tabs";
import Groups from "./screens/groups";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/welcome" element={<Welcome />} />
        <Route path="/about" element={<About />} />
        <Route path="/tabs" element={<Tabs />} />
        <Route path="/groups" element={<Groups />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;