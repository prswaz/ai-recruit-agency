import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { FileText, Briefcase, CheckCircle, TrendingUp, Sparkles, Plus, Users, ArrowRight, Brain, Clock, Bell } from 'lucide-react';
import MatchIntelligenceCard from '../components/MatchIntelligenceCard';
import './Dashboard.css';

const Dashboard = () => {
    const { user } = useAuth();
    const [stats, setStats] = useState({ applications: 0, recommendations: 0, profile_completion: 85 });
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                if (user.role === 'candidate') {
                    // Mocking some API calls for now to focus on UI
                    // In real implementation we would fetch these
                    const [appsResp, recsResp, profileResp, analysisResp] = await Promise.all([
                        api.get('/candidates/applications'),
                        api.get('/candidates/recommendations/'),
                        api.get('/candidates/me'),
                        api.get('/candidates/profile/analysis')
                    ]);

                    setStats({
                        applications: appsResp.data?.length || 0,
                        recommendations: recsResp.data?.length || 0,
                        profile_completion: 85 // Mocked for now
                    });

                    const profileData = profileResp.data;
                    if (analysisResp.data?.has_analysis) {
                        const latest = analysisResp.data.data;
                        profileData.analysis_report = {
                            summary: latest.summary,
                            analysis_results: {
                                strengths: latest.strengths || [],
                                gaps: latest.gaps || []
                            }
                        };
                    }
                    setProfile(profileData);
                }
            } catch (error) {
                console.error("Failed to fetch dashboard data", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [user]);

    if (loading) return (
        <div className="flex-center" style={{ height: '80vh' }}>
            <div className="spinner"></div>
        </div>
    );

    return (
        <div className="page-container dashboard-page">
            <div className="container">
                <header className="page-header mb-8">
                    <div className="header-text">
                        <h1 className="text-3xl font-bold mb-2">Welcome Back, {user.first_name || 'User'} 👋</h1>
                        <p className="text-muted">Here's what's happening with your job search today.</p>
                    </div>
                    <div className="header-actions">
                        <Link to="/resume-upload" className="btn btn-primary">
                            <Plus size={18} /> Upload Resume
                        </Link>
                    </div>
                </header>

                <div className="dashboard-body">
                    {/* Stats Grid with Circular Progress */}
                    <div className="stats-grid mb-8">
                        {/* Profile Completion Circular Widget */}
                        <div className="stat-card circular-stat-card">
                            <div className="circular-progress-wrapper lg">
                                <svg viewBox="0 0 36 36" className="circular-chart-lg">
                                    <path className="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                                    <path className="circle" strokeDasharray={`${stats.profile_completion}, 100`} stroke="var(--primary-color)" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                                    <text x="18" y="20.35" className="percentage">{stats.profile_completion}%</text>
                                </svg>
                            </div>
                            <div className="stat-info-center">
                                <h3>Profile Completion</h3>
                                <p className="text-muted text-sm mt-1">
                                    <span className="text-amber-600 font-medium">Almost there!</span> Complete to unlock matches.
                                </p>
                            </div>
                        </div>

                        {/* Active Applications */}
                        <div className="stat-card">
                            <div className="icon-box bg-blue-100 text-blue-600">
                                <Briefcase size={24} />
                            </div>
                            <div className="stat-content">
                                <h3>{stats.applications}</h3>
                                <p>Active Applications</p>
                            </div>
                        </div>

                        {/* New Recommendations */}
                        <div className="stat-card">
                            <div className="icon-box bg-purple-100 text-purple-600">
                                <Sparkles size={24} />
                            </div>
                            <div className="stat-content">
                                <h3>{stats.recommendations}</h3>
                                <p>AI Matches</p>
                            </div>
                        </div>

                        <div className="stat-card">
                            <div className="icon-box bg-amber-100 text-amber-600">
                                <Bell size={24} />
                            </div>
                            <div className="stat-content">
                                <h3>3</h3>
                                <p>New Alerts</p>
                            </div>
                        </div>
                    </div>

                    <div className="dashboard-main-grid">
                        <div className="main-content-col">
                            {user.role === 'candidate' && profile?.analysis_report ? (
                                <div className="mb-8">
                                    <div className="section-title-row mb-4">
                                        <h2 className="text-xl font-bold">AI Consistency Analysis</h2>
                                    </div>
                                    <MatchIntelligenceCard analysis={profile.analysis_report} />
                                </div>
                            ) : (
                                <div className="card p-8 text-center mb-8">
                                    <Sparkles size={48} className="text-primary mx-auto mb-4" />
                                    <h3 className="text-xl font-bold mb-2">Unlock AI Analysis</h3>
                                    <p className="text-muted mb-6">Upload your resume to get instant match analysis and job recommendations.</p>
                                    <Link to="/profile" className="btn btn-primary">Go to Profile</Link>
                                </div>
                            )}
                        </div>

                        <div className="sidebar-content-col">
                            <div className="card p-6 mb-6">
                                <div className="flex justify-between items-center mb-4">
                                    <h3 className="font-bold flex items-center gap-2 m-0 text-base">
                                        Suggested Actions
                                    </h3>
                                    <div className="tooltip-container">
                                        <div className="info-icon-small">?</div>
                                    </div>
                                </div>

                                <div className="action-list">
                                    <div className="action-item done">
                                        <div className="checkbox-visual checked">
                                            <CheckCircle size={14} className="text-white" />
                                        </div>
                                        <span>Confirm Email Address</span>
                                    </div>
                                    <div className="action-item pending">
                                        <div className="checkbox-visual"></div>
                                        <span>Add "React Native" skill</span>
                                    </div>
                                    <div className="action-item pending">
                                        <div className="checkbox-visual"></div>
                                        <span>Upload Cover Letter</span>
                                    </div>
                                </div>
                            </div>

                            <div className="promo-card premium-glow p-6 rounded-xl text-center relative overflow-hidden">
                                <div className="absolute inset-0 bg-gradient-premium opacity-10"></div>
                                <div className="relative z-10">
                                    <div className="inline-flex items-center justify-center w-10 h-10 rounded-full bg-white/20 mb-3 text-white">
                                        <Sparkles size={20} />
                                    </div>
                                    <h3 className="font-bold text-white mb-2 text-lg">Go Premium</h3>
                                    <p className="text-blue-50 text-sm mb-4">Get unlimited AI matches and priority support.</p>
                                    <button className="btn btn-white w-full shadow-lg hover:scale-105 transition-transform">
                                        Upgrade Plan
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;