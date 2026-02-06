import React from 'react';
import { Github, Twitter, Linkedin, Mail } from 'lucide-react';
import './Footer.css';

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-section brand">
                    <h3>AI Recruiter</h3>
                    <p>Connecting talent with opportunity through intelligent matching.</p>
                </div>
                <div className="footer-section links">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="/jobs">Browse Jobs</a></li>
                        <li><a href="/login">Login</a></li>
                        <li><a href="/register">Sign Up</a></li>
                    </ul>
                </div>
                <div className="footer-section social">
                    <h4>Connect</h4>
                    <div className="social-icons">
                        <a href="#"><Github size={20} /></a>
                        <a href="#"><Twitter size={20} /></a>
                        <a href="#"><Linkedin size={20} /></a>
                        <a href="#"><Mail size={20} /></a>
                    </div>
                </div>
            </div>
            <div className="footer-bottom">
                <p>&copy; {new Date().getFullYear()} AI Recruiter Agency. All rights reserved.</p>
            </div>
        </footer>
    );
};

export default Footer;
