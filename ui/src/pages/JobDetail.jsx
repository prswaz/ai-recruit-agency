import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import './JobDetail.css';
import {
    Briefcase, MapPin, DollarSign, Clock, Building,
    CheckCircle, AlertCircle, ArrowRight, Sparkles,
    Check, Star, Users, Info, ChevronLeft
} from 'lucide-react';

const JobDetail = () => {
    const { id } = useParams();
    const { user } = useAuth();
    const navigate = useNavigate();
    const [job, setJob] = useState(null);
    const [matchData, setMatchData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [applying, setApplying] = useState(false);
    const [message, setMessage] = useState(null);

    useEffect(() => {
        const fetchJob = async () => {
            try {
                const response = await api.get(`/jobs/${id}`);
                setJob(response.data);

                if (user?.role === 'candidate') {
                    try {
                        const matchResponse = await api.get(`/jobs/${id}/match/`);
                        setMatchData(matchResponse.data);
                    } catch (error) {
                        console.error("Error fetching match probability", error);
                    }
                }
            } catch (error) {
                console.error("Error fetching job details", error);
            } finally {
                setLoading(false);
            }
        };
        fetchJob();
    }, [id, user]);

    const handleApply = async () => {
        if (!user) {
            navigate('/login');
            return;
        }

        setApplying(true);
        setMessage(null);

        try {
            await api.post('/candidates/applications/', { job_id: parseInt(id) });
            setMessage({ type: 'success', text: 'Application submitted successfully!' });
        } catch (error) {
            console.error("Application failed", error);
            setMessage({ type: 'error', text: 'Failed to apply. You might have already applied.' });
        } finally {
            setApplying(false);
        }
    };

    if (loading) return <div className="flex-center h-screen"><div className="spinner"></div></div>;
    if (!job) return (
        <div className="page-container flex-center">
            <div className="text-center">
                <AlertCircle size={48} className="mx-auto text-red-500 mb-4" />
                <h2 className="text-2xl font-bold">Job Not Found</h2>
                <button onClick={() => navigate('/jobs')} className="btn btn-primary mt-4">Back to Jobs</button>
            </div>
        </div>
    );

    let requirements = [];
    let benefits = [];

    try {
        requirements = Array.isArray(job.requirements) ? job.requirements : JSON.parse(job.requirements || '[]');
    } catch (e) {
        console.error('Failed to parse requirements:', e);
    }

    try {
        benefits = Array.isArray(job.benefits) ? job.benefits : JSON.parse(job.benefits || '[]');
    } catch (e) {
        console.error('Failed to parse benefits:', e);
    }

    const matchScore = matchData?.match_score || 0;
    const matchColor = matchScore >= 80 ? 'green' : matchScore >= 60 ? 'amber' : 'red';

    return (
        <div className="page-container job-detail-page">
            <div className="container">
                <button onClick={() => navigate(-1)} className="btn-ghost mb-6 flex items-center gap-2 text-muted hover:text-primary transition-colors">
                    <ChevronLeft size={18} /> Back
                </button>

                {/* Job Hero Section */}
                <div className="job-hero">
                    <div className="job-hero-content">
                        <div className="job-title-section">
                            <div className="flex items-center gap-2 text-primary font-bold text-sm uppercase tracking-wider mb-2">
                                <Star size={14} className="fill-current" /> Featured Opportunity
                            </div>
                            <h1 className="text-4xl font-extrabold mb-4">{job.title}</h1>
                            <div className="job-meta-grid">
                                <div className="meta-item"><Building size={18} /> {job.company_name}</div>
                                <div className="meta-item"><MapPin size={18} /> {job.location || 'Remote'}</div>
                                <div className="meta-item"><Briefcase size={18} /> {job.type}</div>
                                {job.salary_range && <div className="meta-item"><DollarSign size={18} /> {job.salary_range}</div>}
                                <div className="meta-item"><Clock size={18} /> {job.experience_level || 'Mid Level'}</div>
                            </div>
                        </div>

                        <div className="job-actions-hero">
                            {user?.role === 'candidate' && (
                                <>
                                    {matchData && matchData.has_resume && (
                                        <div className="match-score-pill">
                                            <Sparkles size={16} /> {matchData.match_score}% Smart Match
                                        </div>
                                    )}
                                    <button
                                        className={`btn btn-primary btn-lg px-8 shadow-lg shadow-primary/20 ${message?.type === 'success' ? 'bg-green-600 border-green-600' : ''}`}
                                        onClick={handleApply}
                                        disabled={applying || message?.type === 'success'}
                                    >
                                        {applying ? 'Sending...' : (message?.type === 'success' ? 'Applied Successfully!' : 'Apply Now')}
                                    </button>
                                </>
                            )}
                        </div>
                    </div>

                    {message && (
                        <div className={`mt-6 p-4 rounded-lg flex items-center gap-3 animate-fade-in ${message.type === 'success' ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-red-50 text-red-700 border border-red-200'}`}>
                            {message.type === 'success' ? <CheckCircle size={20} /> : <AlertCircle size={20} />}
                            <span className="font-medium">{message.text}</span>
                        </div>
                    )}
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8">
                    {/* Main Content */}
                    <div className="lg:col-span-2 space-y-10 detail-content">
                        <section>
                            <h2 className="flex items-center gap-2 text-xl font-bold mb-4">
                                <Info className="text-primary" size={24} /> About the Role
                            </h2>
                            <div className="rich-text whitespace-pre-line leading-relaxed text-secondary">
                                {job.description}
                            </div>
                        </section>

                        {requirements.length > 0 && (
                            <section>
                                <h2 className="flex items-center gap-2 text-xl font-bold mb-4">
                                    <CheckCircle className="text-primary" size={24} /> Requirements
                                </h2>
                                <ul className="list-items space-y-3">
                                    {requirements.map((req, i) => (
                                        <li key={i} className="list-item flex items-start gap-3">
                                            <div className="bullet-point"></div>
                                            <span>{req}</span>
                                        </li>
                                    ))}
                                </ul>
                            </section>
                        )}

                        {benefits.length > 0 && (
                            <section>
                                <h2 className="flex items-center gap-2 text-xl font-bold mb-4">
                                    <Star className="text-primary" size={24} /> Start Benefits
                                </h2>
                                <ul className="list-items space-y-3">
                                    {benefits.map((ben, i) => (
                                        <li key={i} className="list-item flex items-start gap-3">
                                            <Check size={18} className="mt-1 text-green-500 shrink-0" />
                                            <span>{ben}</span>
                                        </li>
                                    ))}
                                </ul>
                            </section>
                        )}
                    </div>

                    {/* Sidebar */}
                    <aside className="job-sidebar" aria-label="Job Sidebar">
                        {/* AI Match Card */}
                        <div className="sidebar-card ai-match-card">
                            <div className="ai-match-header flex items-center gap-2 font-bold mb-4">
                                <Sparkles size={18} className="text-primary" />
                                <span>AI Match Analysis</span>
                            </div>

                            {matchData && matchData.has_resume ? (
                                <>
                                    <div className="match-score-visual">
                                        <div className="score-label-group flex justify-between mb-2 text-sm font-medium">
                                            <span>Compatibility</span>
                                            <span className="score-value font-bold" style={{ color: `var(--accent-${matchColor})` }}>{matchData.match_score}%</span>
                                        </div>
                                        <div className="score-progress-bar h-2 w-full bg-slate-100 rounded-full overflow-hidden" role="progressbar" aria-valuenow={matchData.match_score} aria-valuemin="0" aria-valuemax="100">
                                            <div
                                                className="score-progress-fill h-full transition-all duration-500"
                                                style={{
                                                    width: `${matchData.match_score}%`,
                                                    backgroundColor: matchData.match_score >= 80 ? '#10b981' : matchData.match_score >= 50 ? '#f59e0b' : '#ef4444'
                                                }}
                                            ></div>
                                        </div>
                                        <p className="text-xs text-secondary mt-3 leading-relaxed">
                                            {matchData.match_score >= 80 ? 'Great match! Your skills align perfectly.' :
                                                matchData.match_score >= 50 ? 'Good match, but some skills are missing.' :
                                                    'Low match. Consider highlighting adaptable skills.'}
                                        </p>
                                    </div>

                                    {matchData.matched_skills.length > 0 && (
                                        <div className="skill-tag-group mt-6">
                                            <div className="skill-tag-label text-xs font-bold text-muted mb-2 uppercase">Matched Skills</div>
                                            <div className="skill-chips flex flex-wrap gap-2">
                                                {matchData.matched_skills.map((skill, i) => (
                                                    <span key={i} className="skill-chip match bg-green-50 text-green-700 border border-green-200 px-2 py-1 rounded text-xs font-medium">
                                                        {skill}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {matchData.missing_skills.length > 0 && (
                                        <div className="skill-tag-group mt-4">
                                            <div className="skill-tag-label text-xs font-bold text-muted mb-2 uppercase">Missing Skills</div>
                                            <div className="skill-chips flex flex-wrap gap-2">
                                                {matchData.missing_skills.slice(0, 5).map((skill, i) => (
                                                    <span key={i} className="skill-chip missing bg-red-50 text-red-700 border border-red-100 px-2 py-1 rounded text-xs font-medium">
                                                        {skill}
                                                    </span>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </>
                            ) : (
                                <div className="text-center py-4">
                                    <p className="text-sm text-secondary mb-4">Complete your profile to see your match score.</p>
                                    <button onClick={() => navigate('/profile')} className="btn btn-outline btn-sm w-full font-bold">Complete Profile</button>
                                </div>
                            )}
                        </div>

                        {/* Company Card */}
                        <div className="sidebar-card mt-6">
                            <div className="company-brand flex items-center gap-3 mb-4">
                                <div className="company-logo-large w-12 h-12 bg-indigo-100 text-indigo-600 flex items-center justify-center rounded-xl text-xl font-bold">
                                    {job.company_name?.[0]}
                                </div>
                                <div className="company-details">
                                    <h3 className="font-bold">{job.company_name}</h3>
                                    <p className="text-xs text-muted">Tech & Software</p>
                                </div>
                            </div>
                            <p className="text-sm text-secondary mb-6 leading-relaxed">
                                Building the future of recruiting with AI. Join our fast-paced team.
                            </p>
                            <button className="btn btn-outline w-full flex items-center justify-center gap-2 font-bold">
                                <Users size={16} /> Company Profile
                            </button>
                        </div>
                    </aside>
                </div>
            </div>
        </div>
    );
};

export default JobDetail;