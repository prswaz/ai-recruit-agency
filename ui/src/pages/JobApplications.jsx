import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import './JobApplications.css';
import { User, FileText, Calendar, Check, X, Clock, ArrowRight } from 'lucide-react';

const JobApplications = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [applications, setApplications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [jobTitle, setJobTitle] = useState("");

    useEffect(() => {
        const fetchApplications = async () => {
            try {
                // دریافت جزئیات شغل برای نمایش عنوان
                const jobResp = await api.get(`/jobs/${id}`);
                setJobTitle(jobResp.data.title);

                const response = await api.get(`/jobs/${id}/applications`);
                setApplications(response.data);
            } catch (error) {
                console.error("خطا در دریافت درخواست‌ها", error);
                if (error.response && error.response.status === 403) {
                    alert("شما دسترسی لازم را ندارید");
                    navigate('/dashboard');
                }
            } finally {
                setLoading(false);
            }
        };

        fetchApplications();
    }, [id, navigate]);

    const handleScheduleInterview = async (appId) => {
        const dateStr = prompt("تاریخ مصاحبه را وارد کنید (مثال: 1402-10-15 14:00):", "");
        if (!dateStr) return;

        try {
            await api.post('/interviews/', {
                application_id: appId,
                scheduled_time: dateStr, // در پروژه واقعی باید به فرمت ISO تبدیل شود
                interviewer: "مسئول استخدام"
            });
            alert("مصاحبه با موفقیت زمان‌بندی شد!");
        } catch (error) {
            console.error("خطا در زمان‌بندی", error);
            alert("خطا در ثبت زمان مصاحبه");
        }
    };

    if (loading) return (
        <div className="loading-container" dir="rtl">
            <div className="loader"></div>
            <p>در حال بارگذاری متقاضیان...</p>
        </div>
    );

    return (
        <div className="page-container job-applications-page" dir="rtl">
            <div className="page-header mb-8">
                <button onClick={() => navigate('/dashboard')} className="btn-back">
                    <ArrowRight size={18} /> بازگشت به داشبورد
                </button>
                <h1 className="text-2xl font-bold mt-4">متقاضیان شغل: {jobTitle}</h1>
            </div>

            <div className="applications-list">
                {applications.length === 0 ? (
                    <div className="empty-state glass-panel">
                        <User size={48} className="text-muted" />
                        <p>هنوز درخواستی برای این شغل ثبت نشده است.</p>
                    </div>
                ) : (
                    applications.map(app => (
                        <div key={app.id} className="application-card glass-panel">
                            <div className="applicant-info">
                                <h3 className="font-bold text-lg">{app.full_name}</h3>
                                <div className="info-item">
                                    <User size={14} /> <span>{app.email}</span>
                                </div>
                                <div className="info-item">
                                    <FileText size={14} /> <span>سطح تجربه: {app.experience_level}</span>
                                </div>
                            </div>

                            {app.analysis_report && (
                                <div className="ai-insight-badge">
                                    <div className="match-score">
                                        <span className="label">تطابق هوشمند:</span>
                                        <span className="value">{(app.analysis_report.match_score * 100).toFixed(0)}٪</span>
                                    </div>
                                    <p className="summary-text">
                                        {app.analysis_report.summary.slice(0, 120)}...
                                    </p>
                                </div>
                            )}

                            <div className="actions-area">
                                <a href={app.resume_url} target="_blank" rel="noopener noreferrer" className="btn-outline-sm">
                                    مشاهده رزومه
                                </a>
                                {app.status === 'applied' && (
                                    <button onClick={() => handleScheduleInterview(app.id)} className="btn-primary-sm">
                                        <Calendar size={16} /> زمان‌بندی مصاحبه
                                    </button>
                                )}
                                <div className={`status-tag status-${app.status}`}>
                                    {app.status === 'applied' ? 'بررسی نشده' : app.status}
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default JobApplications;