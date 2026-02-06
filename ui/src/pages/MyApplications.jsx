import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';
import './MyApplications.css';
import {
    Briefcase, MapPin, Clock, CheckCircle,
    XCircle, AlertCircle, ArrowRight, ArrowLeft,
    Calendar, Building, Search
} from 'lucide-react';

const MyApplications = () => {
    const navigate = useNavigate();
    const [applications, setApplications] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchApps = async () => {
            try {
                const response = await api.get('/candidates/applications');
                setApplications(response.data);
            } catch (error) {
                console.error("خطا در دریافت درخواست‌ها", error);
            } finally {
                setLoading(false);
            }
        };

        fetchApps();
    }, []);

    const getStatusBadge = (status) => {
        switch (status) {
            case 'accepted':
                return <span className="status-badge status-accepted"><CheckCircle size={14} /> پذیرفته شده</span>;
            case 'rejected':
                return <span className="status-badge status-rejected"><XCircle size={14} /> رد شده</span>;
            case 'interview_scheduled':
                return <span className="status-badge status-interview"><Calendar size={14} /> مصاحبه</span>;
            default:
                return <span className="status-badge status-pending"><Clock size={14} /> در حال بررسی</span>;
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('fa-IR');
    };

    if (loading) return <div className="flex-center h-screen"><div className="spinner"></div></div>;

    return (
        <div className="page-container applications-page" dir="rtl">
            <div className="container">
                <header className="page-header mb-10">
                    <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
                        <div>
                            <button onClick={() => navigate('/dashboard')} className="btn-ghost mb-2 flex items-center gap-2 text-secondary hover:text-primary transition-colors">
                                <ArrowRight size={16} /> داشبورد
                            </button>
                            <h1 className="text-4xl font-extrabold tracking-tight" style={{ color: '#1e293b' }}>درخواست‌های من</h1>
                            <p className="text-secondary text-lg mt-1">مسیر خود را تا رسیدن به شغل رویایی‌تان دنبال کنید.</p>
                        </div>
                        <div className="flex items-center gap-3 px-4 py-2 bg-slate-100 rounded-full text-slate-600 text-sm font-semibold">
                            <Briefcase size={16} />
                            {applications.length} {applications.length === 1 ? 'درخواست' : 'درخواست'}
                        </div>
                    </div>
                </header>

                {applications.length === 0 ? (
                    <div className="empty-state-card card p-12 text-center max-w-2xl mx-auto shadow-sm">
                        <div className="empty-icon-box mx-auto mb-6">
                            <Search size={40} className="text-indigo-400" />
                        </div>
                        <h3 className="text-2xl font-bold mb-3" style={{ color: '#334155' }}>هنوز درخواستی ثبت نشده است</h3>
                        <p className="text-secondary mb-8 max-w-sm mx-auto">
                            شغل ایده‌آل شما در انتظار است. جستجو را شروع کنید و اجازه دهید هوش مصنوعی ما بهترین فرصت‌ها را به شما پیشنهاد دهد.
                        </p>
                        <Link to="/jobs" className="btn btn-primary px-10 shadow-lg shadow-primary/20">
                            یافتن اولین شغل
                        </Link>
                    </div>
                ) : (
                    <div className="applications-grid">
                        {applications.map(app => (
                            <div key={app.id} className="card application-card hover-lift transition-all duration-300">
                                <div className="card-top p-6 border-b border-slate-50">
                                    <div className="flex justify-between items-start gap-4 mb-4">
                                        <div className="company-logo-mini">
                                            {app.job.company_name?.[0] || 'ش'}
                                        </div>
                                        {getStatusBadge(app.status)}
                                    </div>
                                    <h3 className="text-xl font-bold text-slate-800 mb-1 leading-tight group-hover:text-primary transition-colors">
                                        {app.job.title}
                                    </h3>
                                    <div className="flex items-center gap-2 text-primary font-semibold text-sm mb-4">
                                        <Building size={14} /> {app.job.company_name}
                                    </div>

                                    <div className="space-y-2">
                                        <div className="flex items-center gap-2 text-sm text-secondary">
                                            <MapPin size={14} /> {app.job.location}
                                        </div>
                                        <div className="flex items-center gap-2 text-sm text-secondary">
                                            <Briefcase size={14} /> {app.job.type}
                                        </div>
                                    </div>
                                </div>

                                <div className="card-footer p-6 bg-slate-50/50 flex flex-col gap-4">
                                    <div className="flex items-center justify-between text-xs text-slate-400">
                                        <div className="flex items-center gap-1">
                                            <Calendar size={12} /> تاریخ ثبت درخواست: {formatDate(app.applied_at)}
                                        </div>
                                    </div>

                                    <div className="flex gap-3 mt-2">
                                        <Link to={`/jobs/${app.job.id}`} className="btn btn-outline btn-sm flex-1 justify-center">
                                            جزئیات شغل
                                        </Link>
                                        {app.status === 'interview_scheduled' && (
                                            <Link to="/interviews" className="btn btn-primary btn-sm flex-1 justify-center shadow-sm">
                                                مشاهده مصاحبه
                                            </Link>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default MyApplications;