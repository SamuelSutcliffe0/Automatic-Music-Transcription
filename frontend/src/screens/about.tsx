import React from "react";
import { Link } from "react-router-dom"
 
const About: React.FC = () => {

    return (
        <div>
            <h1>Automatic-Music-Transcription</h1>
            <p>Explore the world of Automatic Music Transcription for guitar. With this helpful tool, guitar melodies can be tranformed into convoinient tablature form, ready for whatever project you require. By utilising Constant-Q-Tranform, this site turns time domain audio tracks into frequency domain, before extracting the note using pitch detection.</p>
            <li> <Link to="/signup">Sign Up Now</Link> </li>
            <li> <Link to="/">Home</Link> </li>
        </div>
        
    );

};
 
export default About;    