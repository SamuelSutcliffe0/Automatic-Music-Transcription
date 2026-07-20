import React, { useState } from 'react';
 
const Login: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        fetch("http://localhost:5000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: new URLSearchParams({
            username: username,
            password: password
        })
        })
        .then(res => res.json())
        .then(data => {
        if (data.error) {
            setError(data.error);
        } else if (data.message === "Login Successful") {
            window.location.href = "/welcome";
        }
        });
        }
        

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
            <button type="submit">Register</button>
        </form>
    </div>
);

};
 
export default Login;