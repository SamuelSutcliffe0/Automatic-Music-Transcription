import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
 
const Tabs: React.FC = () => {
    const navigate = useNavigate();
    const [error, setError] = useState("");

    const handleLogout = async () => {
        setError("");
        try {
            await fetch("http://localhost:5000/logout", {
                method: "POST",
                credentials: "include"
            });
            navigate("/");
        } catch {
            setError("Something went wrong. Please try again.");
        }
    };
    return (
        <div>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <h1>Tabs</h1>
            <p>Tabs Here!</p>
            <li> <Link to="/welcome">Back</Link> </li>
            <button onClick={handleLogout}>Logout</button>
        </div>
        
    );

};
 
export default Tabs;    