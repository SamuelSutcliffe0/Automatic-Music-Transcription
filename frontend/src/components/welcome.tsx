import React from 'react';
import { Link } from 'react-router-dom'
 
const Welcome: React.FC = () => {

    return (
        <div>
            <body>
                <h1>Welcome!</h1>
                <p>You logged in!!!</p>
            </body>
            <li> <Link to="/">Logout</Link> </li>
        </div>
        
    );

};
 
export default Welcome;     