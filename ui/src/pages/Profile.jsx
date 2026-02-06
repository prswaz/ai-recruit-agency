import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { User, Mail, Phone, MapPin, Upload, FileText, Globe, Edit, CheckCircle, AlertCircle, Sparkles, TrendingUp, Shield, Brain, Briefcase } from 'lucide-react';
import AIProcessingTimeline from '../components/AIProcessingTimeline';
import MatchIntelligenceCard from '../components/MatchIntelligenceCard';
import './Profile.css';

const Profile = () => {
    const { user } = useAuth();
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [analysisResult, setAnalysisResult] = useState(null);
    const [message, setMessage] = useState(null);

    // Edit Mode State - Keeping basic edit functionality
    const [isEditing, setIsEditing] = useState(false);
    const [editForm, setEditForm] = useState({
        full_name: '',
        location: '',
        phone: '',
        experience_level: ''
    });

    useEffect(() => {
        if (profile) {
            setEditForm({
                full_name: profile.full_name || '',
                location: profile.location || '',
                phone: profile.phone || '',
                experience_level: profile.experience_level || ''
            });
        }
    }, [profile]);

    useEffect(() => {
        const fetchProfileData = async () => {
            try {
                // Fetch basic profile
                const profileResp = await api.get('/candidates/me');
                setProfile(profileResp.data);

                // Fetch the latest specialized AI analysis
                const analysisResp = await api.get('/candidates/profile/analysis');
                if (analysisResp.data.has_analysis) {
                    const latest = analysisResp.data.data;
                    setAnalysisResult({
                        summary: latest.summary,
                        analysis_results: {
                            strengths: latest.strengths || [],
                            gaps: latest.gaps || []
                        },
                        skills: latest.extracted_skills || [],
                        job_matches: latest.job_matches || {}
                    });
                } else if (profileResp.data.analysis_report) {
                    setAnalysisResult(profileResp.data.analysis_report);
                }
            } catch (error) {
                console.error("Failed to fetch profile or analysis", error);
                setMessage({ type: 'error', text: 'Could not load profile. Please try logging in again.' });
            } finally {
                setLoading(false);
            }
        };
        fetchProfileData();
    }, []);

    const handleUpdate = async (e) => {
        e.preventDefault();
        try {
            await api.patch('/candidates/me', editForm);
            const profileResp = await api.get('/candidates/me');
            setProfile(profileResp.data);
            setIsEditing(false);
            setMessage({ type: 'success', text: 'Profile updated successfully!' });
            setTimeout(() => setMessage(null), 3000);
        } catch (error) {
            console.error("Update failed", error);
            setMessage({ type: 'error', text: 'Failed to update profile.' });
        }
    };

    const handleInputChange = (e) => {
        setEditForm({ ...editForm, [e.target.name]: e.target.value });
    };

    if (loading) return <div className="flex-center h-screen"><div className="spinner"></div></div>;

    if (!profile) return (
        <div className="page-container">
            <div className="container">
                <div className="card p-8 text-center">
                    <AlertCircle size={48} className="mx-auto text-red-500 mb-4" />
                    <h2 className="text-xl font-bold">Profile Not Found</h2>
                    <p className="text-muted">We couldn't load your profile information.</p>
                </div>
            </div>
        </div>
    );

    // Calculate generic progress stats (mock or real if available)
    const skillsCount = profile.skills?.length || 0;
    const skillsProgress = Math.min(skillsCount * 10, 100); // 10 skills = 100%
    const experienceProgress = profile.experience_level === 'Senior' ? 90 : profile.experience_level === 'Mid-Level' ? 60 : 30;

    return (
        <div className="page-container profile-page">
            <div className="container">
                {/* Profile Header Card */}
                <div className="profile-header-card mb-8 animate-fade-in">
                    <div className="profile-cover"></div>
                    <div className="profile-content-wrapper">
                        <div className="profile-avatar-wrapper">
                            <div className="profile-avatar">
                                {profile.full_name?.[0] || <User size={40} />}
                            </div>
                        </div>

                        <div className="profile-info-header">
                            <div className="info-main">
                                <h1 className="profile-name">{profile.full_name}</h1>
                                <p className="profile-role">
                                    {profile.experience_level || 'Open for work'} • {profile.location || 'Location not set'}
                                </p>
                                <div className="profile-contacts">
                                    <span className="contact-item"><Mail size={14} /> {profile.email}</span>
                                    {profile.phone && <span className="contact-item"><Phone size={14} /> {profile.phone}</span>}
                                </div>
                            </div>
                            <div className="profile-actions">
                                <button className="btn btn-secondary" onClick={() => setIsEditing(true)}>
                                    <Edit size={16} className="mr-2" /> Edit Profile
                                </button>
                                <Link to="/resume-upload" className="btn btn-primary">
                                    <Upload size={16} className="mr-2" /> Update Resume
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>

                {message && (
                    <div className={`mb-6 p-4 rounded-xl flex items-center gap-3 ${message.type === 'error' ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-green-50 text-green-700 border border-green-200'}`}>
                        {message.type === 'error' ? <AlertCircle size={20} /> : <CheckCircle size={20} />}
                        {message.text}
                    </div>
                )}

                <div className="profile-main-grid">
                    {/* Left Column: Stats & Skills */}
                    <div className="left-col">
                        {/* Progress Section */}
                        <div className="card mb-6">
                            <h3 className="card-title mb-4">Profile Strength</h3>

                            <div className="progress-item mb-4">
                                <div className="flex justify-between mb-1">
                                    <span className="text-sm font-semibold text-secondary">Skills Identified</span>
                                    <span className="text-sm font-bold text-primary">{skillsProgress}%</span>
                                </div>
                                <div className="progress-bar-bg">
                                    <div className="progress-bar-fill" style={{ width: `${skillsProgress}%` }}></div>
                                </div>
                            </div>

                            <div className="progress-item mb-4">
                                <div className="flex justify-between mb-1">
                                    <span className="text-sm font-semibold text-secondary">Experience Level</span>
                                    <span className="text-sm font-bold text-primary">{experienceProgress}%</span>
                                </div>
                                <div className="progress-bar-bg">
                                    <div className="progress-bar-fill bg-success" style={{ width: `${experienceProgress}%` }}></div>
                                </div>
                            </div>
                        </div>

                        {/* Resume Status */}
                        <div className="card mb-6">
                            <h3 className="card-title mb-4 flex items-center gap-2">
                                <FileText size={18} className="text-primary" /> Resume Status
                            </h3>
                            {profile.resume_url ? (
                                <div className="resume-status-box active">
                                    <div className="icon-circle bg-green-100 text-green-600">
                                        <CheckCircle size={20} />
                                    </div>
                                    <div>
                                        <p className="font-bold text-main">Resume Active</p>
                                        <p className="text-xs text-muted">Last updated recently</p>
                                    </div>
                                </div>
                            ) : (
                                <div className="resume-status-box inactive">
                                    <div className="icon-circle bg-amber-100 text-amber-600">
                                        <AlertCircle size={20} />
                                    </div>
                                    <div>
                                        <p className="font-bold text-main">No Resume</p>
                                        <p className="text-xs text-muted">Upload to get matches</p>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Skills Section */}
                        <div className="card mb-8">
                            <div className="flex justify-between items-center mb-6">
                                <h2 className="text-xl font-bold flex items-center gap-2">
                                    <Code size={20} className="text-primary" /> Skills
                                </h2>
                                {!isEditing && (
                                    <button className="btn-icon text-muted hover:text-primary">
                                        <Edit2 size={18} />
                                    </button>
                                )}
                            </div>

                            {profile.skills && profile.skills.length > 0 ? (
                                <div className="skills-container flex flex-wrap gap-2">
                                    {profile.skills.map((skill, index) => (
                                        <span key={index} className="skill-badge px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-sm font-medium">
                                            {skill}
                                        </span>
                                    ))}
                                </div>
                            ) : (
                                <div className="bg-slate-50 rounded-xl p-8 text-center border border-dashed border-slate-200">
                                    <p className="text-muted mb-4">No skills added yet. Add skills to get better job matches.</p>
                                    <button className="btn btn-sm btn-outline btn-primary">
                                        + Add Skills
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Right Column: AI Analysis */}
                    <div className="right-col">
                        {analysisResult ? (
                            <MatchIntelligenceCard analysis={analysisResult} />
                        ) : (
                            <div className="empty-analysis-state">
                                <div className="empty-icon-box">
                                    <Sparkles size={40} className="text-primary" />
                                </div>
                                <h3>No Analysis Available</h3>
                                <p>Upload your resume to unlock detailed AI insights about your career profile and job matches.</p>
                                <Link to="/resume-upload" className="btn btn-primary mt-4">
                                    Upload Resume Now
                                </Link>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Edit Modal */}
            {isEditing && (
                <div className="modal-overlay">
                    <div className="modal-card">
                        <div className="modal-header">
                            <h2 className="text-xl font-bold">Edit Profile</h2>
                            <button onClick={() => setIsEditing(false)} className="btn-icon">
                                <AlertCircle size={20} className="rotate-45" /> {/* Using AlertCircle as close icon fallback if X not imported, though usually X */}
                            </button>
                        </div>
                        <form onSubmit={handleUpdate} className="space-y-4">
                            <div>
                                <label className="label">Full Name</label>
                                <input type="text" name="full_name" value={editForm.full_name} onChange={handleInputChange} className="input" required />
                            </div>
                            <div>
                                <label className="label">Phone</label>
                                <input type="text" name="phone" value={editForm.phone} onChange={handleInputChange} className="input" />
                            </div>
                            <div>
                                <label className="label">Location</label>
                                <input type="text" name="location" value={editForm.location} onChange={handleInputChange} className="input" />
                            </div>
                            <div>
                                <label className="label">Experience Level</label>
                                <select name="experience_level" value={editForm.experience_level} onChange={handleInputChange} className="input">
                                    <option value="">Select Level</option>
                                    <option value="Junior">Junior (0-2 yrs)</option>
                                    <option value="Mid-Level">Mid-Level (3-5 yrs)</option>
                                    <option value="Senior">Senior (6+ yrs)</option>
                                    <option value="Lead">Lead</option>
                                    <option value="Executive">Executive</option>
                                </select>
                            </div>
                            <div className="flex justify-end gap-3 mt-6">
                                <button type="button" className="btn btn-secondary" onClick={() => setIsEditing(false)}>Cancel</button>
                                <button type="submit" className="btn btn-primary">Save Changes</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Profile;
