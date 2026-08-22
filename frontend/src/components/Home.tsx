import React from 'react';
import { Link } from 'react-router-dom'
 
const Home: React.FC = () => {

    return (
        <div>
            <li> <Link to="/signup">Sign Up</Link> </li>
            <li> <Link to="/login">Log In</Link> </li>
        </div>
        
    );

};
 
export default Home;     