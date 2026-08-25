import React, { useState } from "react";
import { useNavigate} from "react-router-dom"
 
const AdminSQLTerminal: React.FC = () => {
    const [query, setQuery] = useState("")
    const [response, setResponse] = useState("")
    const [error, setError] = useState("");
    const navigate = useNavigate()

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setError("");
        setResponse("");

        try {
            const res = await fetch("http://localhost:5000/admin_SQL", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({
                    query
                })
            });

            const data = await res.json();

            if (data.error) return setError(data.error);
            if (data.message === "No Response")  return  setResponse("No Output");
            else return setResponse(data.message)
        } catch {
            setError("Something went wrong. Please try again.");
        }
        
    };

    const handleAdminLogout = async () => {
        setError("");
        try {
            await fetch("http://localhost:5000/admin_logout", {
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
        <h1>Admin SQL Terminal</h1>
        <p>Use this terminal to make manual edits to the SQL database</p>
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Enter SQL Query Here"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
            <button type="submit">Execute Query</button>
        </form>
        <p dangerouslySetInnerHTML={{ __html: response }} />
        <button onClick={handleAdminLogout}>Logout</button>
    </div>
);

};


export default AdminSQLTerminal;