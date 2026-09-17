import React, { useState } from "react";
import { useNavigate} from "react-router-dom"
 
const Upload: React.FC = () => {

    const navigate = useNavigate();
    const [error, setError] = useState("");
    const [tab, setTab] = useState(JSON);

    const handlePolling = async () => {
        setError("");

        while (true) {
        try{
            const res = await fetch("http://localhost:5000/upload", {
                method: "POST",
                credentials: "include"
            });
            const data = await res.json();
            if (data.message) return setTab(data.message);
            if (data.error) return setError(data.error);
        } catch{setError("Something went wrong. Please try again.");}}; 
        };

    


};

export default Upload;