import React from 'react';
import { Link } from 'react-router-dom'
 
const Home: React.FC = () => {

    return (
        <div>
            <li> <Link to="/signup">Signup</Link> </li>
            <li> <Link to="/login">Login</Link> </li>
        </div>
        
    );

};
 
export default Home;     