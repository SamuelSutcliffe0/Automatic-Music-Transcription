import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
 
const Tabs: React.FC = () => {
    const navigate = useNavigate();
    const [error, setError] = useState("");
    const [tabs, setTabs] = useState("");

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

    const handleDisplayTabs = async () => {
        setError("");
        try {
            const res = await fetch("http://localhost:5000/display_tabs", {
                method: "GET",
                credentials: "include"
            });
            const data = await res.json();
            if (data.error) return setError(data.error);
            if (data.message) return setTabs(data.message);
            ;
        } catch {
            setError("Something went wrong. Please try again.");
        }
    };

    useEffect(() => {
        handleDisplayTabs();
    }, []);

    return (
        <div>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <h1>Tabs:</h1>
            <p>{tabs}</p>
            <li> <Link to="/welcome">Back</Link> </li>
            <button onClick={handleLogout}>Logout</button>
        </div>
        
    );

};
 
export default Tabs;    