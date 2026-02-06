import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Brain, Shield, Users, Sparkles, CheckCircle, TrendingUp } from 'lucide-react';
import './Landing.css';

const Landing = () => {
    return (
        <div className="landing-page">
            {/* Hero Section */}
            <section className="hero-section">
                <div className="container hero-container">
                    <div className="hero-content">
                        <div className="badge badge-info mb-4 animate-fade-in">
                            <Sparkles size={14} className="mr-2" /> AI-Powered Recruiting
                        </div>
                        <h1 className="hero-title animate-fade-in" style={{ animationDelay: '0.1s' }}>
                            Find Your <br />
                            <span className="text-gradient">Perfect Job Match</span>
                        </h1>
                        <p className="hero-subtitle animate-fade-in" style={{ animationDelay: '0.2s' }}>
                            Stop searching endlessly. Our AI analyzes your profile and matches you with top companies in seconds.
                        </p>
                        <div className="hero-actions animate-fade-in" style={{ animationDelay: '0.3s' }}>
                            <Link to="/register" className="btn btn-primary btn-lg">
                                Start Matching <ArrowRight size={18} />
                            </Link>
                            <Link to="/jobs" className="btn btn-secondary btn-lg">
                                Browse Jobs
                            </Link>
                        </div>

                        <div className="hero-stats animate-fade-in" style={{ animationDelay: '0.4s' }}>
                            <div className="stat-item">
                                <span className="stat-number">10k+</span>
                                <span className="stat-label">Active Jobs</span>
                            </div>
                            <div className="stat-divider"></div>
                            <div className="stat-item">
                                <span className="stat-number">95%</span>
                                <span className="stat-label">Match Rate</span>
                            </div>
                            <div className="stat-divider"></div>
                            <div className="stat-item">
                                <span className="stat-number">500+</span>
                                <span className="stat-label">Companies</span>
                            </div>
                        </div>
                    </div>

                    <div className="hero-visual animate-fade-in" style={{ animationDelay: '0.5s' }}>
                        <div className="visual-circle-bg"></div>
                        <div className="glass-panel match-card">
                            <div className="match-header">
                                <div className="match-avatar">JD</div>
                                <div className="match-info">
                                    <div className="match-name">John Doe</div>
                                    <div className="match-role">Senior Developer</div>
                                </div>
                                <div className="match-score">98%</div>
                            </div>
                            <div className="match-body">
                                <div className="skill-tag"><CheckCircle size={12} /> React</div>
                                <div className="skill-tag"><CheckCircle size={12} /> Node.js</div>
                                <div className="skill-tag"><CheckCircle size={12} /> Python</div>
                            </div>
                        </div>

                        <div className="glass-panel stat-float float-1">
                            <div className="flex items-center gap-2">
                                <TrendingUp size={20} className="text-primary" />
                                <div>
                                    <div className="text-xs text-muted">Interview Success</div>
                                    <div className="font-bold">+124%</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="features-section">
                <div className="container">
                    <div className="section-header text-center mb-8">
                        <h2 className="section-title">Why Choose AI Recruiter?</h2>
                        <p className="section-desc">We represent the future of hiring.</p>
                    </div>

                    <div className="grid-cols-3 features-grid gap-8">
                        <div className="card feature-card hover:scale-105 transition-transform duration-300">
                            <div className="icon-wrapper bg-blue-100 text-blue-600">
                                <Brain size={32} />
                            </div>
                            <h3>Smart Matching</h3>
                            <p className="text-muted">Our advanced algorithms analyze thousands of data points to find the perfect fit.</p>
                        </div>
                        <div className="card feature-card hover:scale-105 transition-transform duration-300">
                            <div className="icon-wrapper bg-green-100 text-green-600">
                                <Users size={32} />
                            </div>
                            <h3>Bias-Free Hiring</h3>
                            <p className="text-muted">Focus on skills and experience. We eliminate bias to reveal true potential.</p>
                        </div>
                        <div className="card feature-card hover:scale-105 transition-transform duration-300">
                            <div className="icon-wrapper bg-purple-100 text-purple-600">
                                <Shield size={32} />
                            </div>
                            <h3>Verified Profiles</h3>
                            <p className="text-muted">Trust is key. We verify qualifications and background checks automatically.</p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
};

export default Landing;
