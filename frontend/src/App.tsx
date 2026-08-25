import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./screens/home";
import Login from "./screens/login";
import Signup from "./screens/signup";
import Welcome from "./screens/welcome";
import About from "./screens/about";
import Tabs from "./screens/tabs";
import Groups from "./screens/groups";
import AdminSQLTerminal from "./screens/admin_SQL"
import AdminLogin from "./screens/admin_login";

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
        <Route path="/admin_SQL" element={<AdminSQLTerminal />} />
        <Route path="/admin_login" element={<AdminLogin />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;