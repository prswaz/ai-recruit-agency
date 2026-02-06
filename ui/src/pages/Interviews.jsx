import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Calendar, CheckCircle, XCircle, Clock, Video, AlertCircle } from 'lucide-react';
import './Interviews.css';

const Interviews = () => {
    const [interviews, setInterviews] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchInterviews = async () => {
            try {
                const response = await api.get('/interviews/');
                setInterviews(response.data);
            } catch (error) {
                console.error("Failed to fetch interviews", error);
            } finally {
                setLoading(false);
            }
        };

        fetchInterviews();
    }, []);

    const getStatusBadge = (status) => {
        switch (status) {
            case 'passed': return <span className="badge badge-green flex items-center gap-1"><CheckCircle size={12} /> Passed</span>;
            case 'failed': return <span className="badge badge-red flex items-center gap-1"><XCircle size={12} /> Failed</span>;
            default: return <span className="badge badge-yellow flex items-center gap-1"><Clock size={12} /> Scheduled</span>;
        }
    };

    if (loading) return <div className="flex-center h-screen"><div className="spinner"></div></div>;

    return (
        <div className="page-container">
            <div className="page-header mb-8">
                <h1>My Interviews</h1>
                <p>Track your interview schedule and results</p>
            </div>

            <div className="space-y-6">
                {interviews.length > 0 ? (
                    interviews.map(interview => (
                        <div key={interview.id} className="card p-6 flex flex-col md:flex-row gap-6 items-start">
                            {/* Date Box */}
                            <div className="bg-indigo-50 text-indigo-700 rounded-lg p-4 text-center min-w-[100px]">
                                <div className="text-xs font-bold uppercase tracking-wider mb-1">{new Date(interview.date).toLocaleDateString(undefined, { month: 'short' })}</div>
                                <div className="text-2xl font-bold mb-1">{new Date(interview.date).getDate()}</div>
                                <div className="text-xs">{new Date(interview.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
                            </div>

                            <div className="flex-1 w-full">
                                <div className="flex justify-between items-start mb-2">
                                    <div>
                                        <h3 className="font-bold text-lg text-slate-900">{interview.job_title}</h3>
                                        <p className="text-indigo-600 font-medium">{interview.company}</p>
                                    </div>
                                    {getStatusBadge(interview.status)}
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                                    <div className="flex items-center gap-2 text-sm text-secondary">
                                        <Video size={16} />
                                        <span>Video Interview</span>
                                    </div>
                                    <div className="flex items-center gap-2 text-sm text-secondary">
                                        <CheckCircle size={16} />
                                        <span>Interviewer: {interview.interviewer || 'Hiring Manager'}</span>
                                    </div>
                                </div>

                                {interview.feedback && (
                                    <div className="mt-4 bg-slate-50 p-4 rounded-lg border border-slate-200">
                                        <h4 className="font-semibold text-sm mb-1 text-slate-700">Feedback</h4>
                                        <p className="text-sm text-slate-600 italic">"{interview.feedback}"</p>
                                    </div>
                                )}
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="col-span-full text-center py-16 bg-slate-50 rounded-xl border-dashed border-2 border-slate-200">
                        <Calendar size={48} className="mx-auto text-slate-300 mb-4" />
                        <h3 className="text-lg font-semibold text-slate-700 mb-2">No Interviews Yet</h3>
                        <p className="text-secondary">When you are shortlisted, your interviews will appear here.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Interviews;
