import React, { useCallback, useState } from "react";
import { Link } from 'react-router-dom';
import { useDropzone } from "react-dropzone";
import axios from "axios";

const Upload: React.FC = () => {
    const [message, setMessage] = useState("Upload Audio Files Here (.wav)");
    const [error, setError] = useState("");

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        setError("");
        setMessage("Loading...");

        try {
            const formData = new FormData();
            formData.append("file", acceptedFiles[0]);

            const res = await axios.post(
                "http://localhost:5000/upoad_tab",
                formData,
                { headers: { "Content-Type": "multipart/form-data" } }
            );
            
            if (res.data.message === "upload successful") {
                setMessage("Upload successful");

                setTimeout(() => {
                    setMessage("Upload Audio Files Here (.wav)");
                }, 5000);
            } else if (res.data.error) {
                setError(res.data.error);
                setMessage("Upload Audio Files Here (.wav)");
            } else {
                setError("Unexpected response from server.");
                setMessage("Upload Audio Files Here (.wav)");
            }

        } catch {
            setError("Something went wrong. Please try again.");
            setMessage("Upload Audio Files Here (.wav)");
        }
    }, []);

    const { getRootProps, getInputProps } = useDropzone({
        onDrop,
        multiple: false,
    });

    return (
        <div>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <div {...getRootProps()}>
                <input {...getInputProps()} />
                <p>{message}</p>
            </div>
            <li> <Link to="/welcome">Back</Link> </li>
        </div>
    );
};

export default Upload;
