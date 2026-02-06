import React, { useState, useEffect } from 'react';
import api from '../services/api';
import './AnalysisHistory.css';
import { FileText, Calendar, CheckCircle, AlertCircle, ChevronLeft, Download } from 'lucide-react';

const AnalysisHistory = () => {
    const [analyses, setAnalyses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            setLoading(true);
            const response = await api.get('/candidates/analysis-history/');
            setAnalyses(response.data);
            setLoading(false);
        } catch (err) {
            console.error('Error fetching analysis history:', err);
            setError('Could not load analysis history. Please try again.');
            setLoading(false);
        }
    };

    const formatDate = (dateString) => {
        const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
        return new Date(dateString).toLocaleDateString('en-US', options);
    };

    if (loading) {
        return (
            <div className="analysis-history-page page-container">
                <div className="container">
                    <div className="loading-state">
                        <div className="loader"></div>
                        <p>Loading your analysis history...</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="analysis-history-page page-container">
            <div className="container">
                <header className="page-header mb-8">
                    <h1 className="text-3xl font-bold mb-2">Analysis Insights</h1>
                    <p className="text-secondary">Track your resume improvements and AI insights over time.</p>
                </header>

                {error && <div className="error-message">{error}</div>}

                {!loading && analyses.length === 0 ? (
                    <div className="empty-state glass-panel">
                        <FileText size={48} />
                        <h3>No Analyses Found</h3>
                        <p>Upload your first resume on the profile page to get started!</p>
                    </div>
                ) : (
                    <div className="analysis-list">
                        {analyses.map((analysis) => (
                            <div key={analysis.id} className="analysis-card glass-panel">
                                <div className="analysis-card-header">
                                    <div className="analysis-meta">
                                        <div className="date-badge">
                                            <Calendar size={14} />
                                            <span>{formatDate(analysis.created_at)}</span>
                                        </div>
                                        <h3 className="analysis-title">Resume Analysis</h3>
                                    </div>
                                    <a href={analysis.resume_url} target="_blank" rel="noopener noreferrer" className="btn btn-outline btn-sm">
                                        <Download size={14} />
                                        View Resume
                                    </a>
                                </div>

                                <div className="analysis-content">
                                    <div className="analysis-summary">
                                        <h4>AI Summary</h4>
                                        <p>{analysis.summary || 'No summary available for this analysis.'}</p>
                                    </div>

                                    <div className="analysis-grid">
                                        <div className="analysis-section">
                                            <header>
                                                <CheckCircle size={16} className="text-success" />
                                                <h5>Key Strengths</h5>
                                            </header>
                                            <ul>
                                                {analysis.strengths && analysis.strengths.slice(0, 3).map((strength, i) => (
                                                    <li key={i}>{strength}</li>
                                                ))}
                                                {(!analysis.strengths || analysis.strengths.length === 0) && (
                                                    <li className="text-muted">No specific strengths listed.</li>
                                                )}
                                            </ul>
                                        </div>

                                        <div className="analysis-section">
                                            <header>
                                                <AlertCircle size={16} className="text-warning" />
                                                <h5>Growth Areas</h5>
                                            </header>
                                            <ul>
                                                {analysis.gaps && analysis.gaps.slice(0, 3).map((gap, i) => (
                                                    <li key={i}>{gap}</li>
                                                ))}
                                                {(!analysis.gaps || analysis.gaps.length === 0) && (
                                                    <li className="text-muted">No specific gaps identified.</li>
                                                )}
                                            </ul>
                                        </div>
                                    </div>

                                    <div className="skills-detected">
                                        <h5>Detected Skills</h5>
                                        <div className="skill-tags">
                                            {analysis.extracted_skills && analysis.extracted_skills.map((skill, i) => (
                                                <span key={i} className="skill-pill">{skill}</span>
                                            ))}
                                            {(!analysis.extracted_skills || analysis.extracted_skills.length === 0) && (
                                                <span className="text-muted">No skills detected.</span>
                                            )}
                                        </div>
                                    </div>
                                </div>

                                <div className="analysis-card-footer">
                                    <div className="match-stats">
                                        Found <strong>{analysis.job_matches?.matched_jobs?.length || 0}</strong> top job matches
                                    </div>
                                    <button className="btn btn-link btn-sm" onClick={() => {/* Future detail view */ }}>
                                        Full Report <ChevronLeft size={14} className="rotate-180" />
                                    </button>
                                </div>

                                {analysis.job_matches?.matched_jobs?.length > 0 && (
                                    <div className="matched-jobs-section">
                                        <h5>Top Matched Jobs</h5>
                                        <div className="matched-jobs-list">
                                            {analysis.job_matches.matched_jobs.map((job, idx) => (
                                                <div key={idx} className="matched-job-item">
                                                    <div className="job-info">
                                                        <h6>{job.title}</h6>
                                                        <p>{job.company} • {job.location}</p>
                                                    </div>
                                                    <div className="job-score">
                                                        <div className="score-ring">
                                                            {job.match_score}
                                                        </div>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default AnalysisHistory;