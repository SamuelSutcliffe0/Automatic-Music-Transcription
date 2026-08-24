import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';

const Welcome: React.FC = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
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

    const handleSessionUser = async () => {
        setError("");
        try {
            const res = await fetch("http://localhost:5000/welcome", {
                method: "GET",
                credentials: "include"
            });

            const data = await res.json();
            if (data.error) return setError(data.error);
            if (data.message) return setUsername(data.message);
        } catch {
            setError("Something went wrong. Please try again.");
        }
    };

    useEffect(() => {
        handleSessionUser();
    }, []);

    return (
        <div>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <h1>Welcome {username}!</h1>
            <p>You logged in!!!</p>
            <li> <Link to="/tabs">View Your Tabs</Link> </li>
            <li> <Link to="/groups">View Your Groups</Link> </li>
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
};

export default Welcome;
