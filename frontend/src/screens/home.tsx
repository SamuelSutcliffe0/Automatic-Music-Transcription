import React from "react";
import { Link } from "react-router-dom"
 
const Home: React.FC = () => {

    return (
        <div>
            <h1>Home Page</h1>
            <li> <Link to="/about">About</Link> </li>
            <li> <Link to="/signup">Sign Up</Link> </li>
            <li> <Link to="/login">Log In</Link> </li>
            <li> <Link to="/admin_login">Admin Log In</Link> </li>
        </div>
        
    );

};
 
export default Home;    