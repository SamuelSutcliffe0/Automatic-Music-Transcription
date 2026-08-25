import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom"
 
const AdminLogin: React.FC = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const redirect = useNavigate()
    

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setError("");

        try {
            const res = await fetch("http://localhost:5000/admin_login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({
                    username,
                    password,
                })
            });

            const data = await res.json();

            if (data.error) return setError(data.error);
            if (data.message === "Login Successful")  redirect("/admin_SQL");
        } catch {
            setError("Something went wrong. Please try again.");
        }
        
    };

    return (
    <div>
        {error && <p style={{ color: "red" }}>{error}</p>}
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button type="submit">Admin Log In</button>
        </form>
        <li> <Link to="/">Home</Link> </li>
    </div>
);

};


export default AdminLogin;