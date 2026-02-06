import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import './PostJob.css';
import {
    Briefcase, MapPin, DollarSign, List,
    CheckCircle, AlertCircle, Building,
    Sparkles, ArrowLeft, Info, PlusCircle,
    Check
} from 'lucide-react';

const PostJob = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [hasCompany, setHasCompany] = useState(true); // Default to true, check on mount
    const [formData, setFormData] = useState({
        title: '',
        location: '',
        type: 'Full-time',
        experience_level: 'Mid-Level',
        salary_range: '',
        description: '',
        requirements: '',
        benefits: ''
    });
    const [loading, setLoading] = useState(false);
    const [checkLoading, setCheckLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const checkUserStatus = async () => {
            if (user?.role !== 'recruiter') {
                setCheckLoading(false);
                return;
            }

            try {
                // Check if recruiter has any companies
                const response = await api.get('/candidates/me'); // Using me endpoint to check role data
                // In this system, companies are linked via user.companies.
                // We'll trust the backend validation but can proactively check if profile allows
                const profileResp = await api.get('/candidates/me');
                // The recruiter check in views.py perform_create is the source of truth
                setCheckLoading(false);
            } catch (err) {
                console.error("Status check failed", err);
                setCheckLoading(false);
            }
        };
        checkUserStatus();
    }, [user]);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const payload = {
                ...formData,
                requirements: formData.requirements.split('\n').filter(line => line.trim()),
                benefits: formData.benefits.split('\n').filter(line => line.trim())
            };

            await api.post('/jobs/', payload);
            navigate('/dashboard');
        } catch (err) {
            console.error("Failed to post job", err);
            const backendError = err.response?.data?.error || err.response?.data?.detail || 'Failed to create job posting. Please try again.';

            // If it's a specific "missing company" error, we can handle it UI-wise
            if (typeof backendError === 'string' && backendError.includes('company profile')) {
                setHasCompany(false);
            }

            // Handle nested serializer errors
            if (typeof backendError === 'object') {
                setError(Object.values(backendError).flat().join(' '));
            } else {
                setError(backendError);
            }
        } finally {
            setLoading(false);
        }
    };

    if (checkLoading) return <div className="flex-center h-screen"><div className="spinner"></div></div>;

    // Role guard
    if (user?.role !== 'recruiter') {
        return (
            <div className="page-container flex-center">
                <div className="card p-8 text-center max-w-md">
                    <AlertCircle size={48} className="mx-auto text-amber-500 mb-4" />
                    <h2 className="text-2xl font-bold mb-2">Recruiter Access Only</h2>
                    <p className="text-secondary mb-6">
                        Posting jobs is restricted to recruiters. If you are looking for jobs, please visit the Job Listings page.
                    </p>
                    <Link to="/jobs" className="btn btn-primary w-full">View Job Opportunities</Link>
                </div>
            </div>
        );
    }

    // Company Setup guard
    if (!hasCompany) {
        return (
            <div className="page-container">
                <div className="container mt-12">
                    <div className="company-setup-card max-w-2xl mx-auto">
                        <div className="setup-icon-box">
                            <Building size={32} />
                        </div>
                        <h2 className="text-3xl font-bold mb-4">Complete Your Company Profile</h2>
                        <p className="text-secondary mb-8 text-lg">
                            To post a job, you first need to create your company profile so candidates know who they are applying to.
                        </p>
                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <button onClick={() => setHasCompany(true)} className="btn btn-primary px-8">
                                Create Company Profile
                            </button>
                            <Link to="/dashboard" className="btn btn-secondary px-8">
                                Back to Dashboard
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="page-container post-job-page">
            <div className="container">
                <div className="max-w-4xl mx-auto">
                    <div className="flex items-center justify-between mb-8">
                        <div>
                            <button onClick={() => navigate(-1)} className="btn-ghost mb-2 flex items-center gap-2 text-secondary hover:text-primary transition-colors">
                                <ArrowLeft size={16} /> Back
                            </button>
                            <h1 className="text-4xl font-extrabold" style={{ color: '#1e293b' }}>Post a New Job</h1>
                            <p className="text-secondary text-lg">Our AI engine helps you find the best talent.</p>
                        </div>
                        <div className="hidden md:block">
                            <div className="flex items-center gap-3 px-4 py-2 bg-indigo-50 text-indigo-700 rounded-full border border-indigo-100">
                                <Sparkles size={18} />
                                <span className="font-semibold text-sm">AI-Optimized Job Posting</span>
                            </div>
                        </div>
                    </div>

                    <div className="form-container">
                        {error && (
                            <div className="bg-red-50 text-red-700 border border-red-200 p-4 rounded-xl mb-8 flex items-start gap-3 animate-in fade-in slide-in-from-top-4">
                                <AlertCircle size={20} className="mt-0.5 flex-shrink-0" />
                                <div className="font-medium text-sm">{error}</div>
                            </div>
                        )}

                        <form onSubmit={handleSubmit} className="space-y-8">
                            <section>
                                <h2 className="section-title"><Info size={18} /> اطلاعات موقعیت شغلی</h2>
                                <div className="form-grid">
                                    <div className="form-group full-width">
                                        <label className="label">عنوان شغلی</label>
                                        <div className="input-wrapper">
                                            <Briefcase size={18} className="input-icon" />
                                            <input
                                                type="text"
                                                name="title"
                                                value={formData.title}
                                                onChange={handleChange}
                                                className="input pr-10"
                                                placeholder="مثال: مهندس ارشد یادگیری ماشین"
                                                required
                                            />
                                        </div>
                                    </div>

                                    <div className="form-group">
                                        <label className="label">محل کار</label>
                                        <div className="input-wrapper">
                                            <MapPin size={18} className="input-icon" />
                                            <input
                                                type="text"
                                                name="location"
                                                value={formData.location}
                                                onChange={handleChange}
                                                className="input pr-10"
                                                placeholder="مثال: دورکاری، تهران"
                                                required
                                            />
                                        </div>
                                    </div>

                                    <div className="form-group">
                                        <label className="label">بازه حقوق</label>
                                        <div className="input-wrapper">
                                            <DollarSign size={18} className="input-icon" />
                                            <input
                                                type="text"
                                                name="salary_range"
                                                value={formData.salary_range}
                                                onChange={handleChange}
                                                className="input pr-10"
                                                placeholder="مثال: ۲۰ - ۳۰ میلیون تومان"
                                            />
                                        </div>
                                    </div>

                                    <div className="form-group">
                                        <label className="label">نوع همکاری</label>
                                        <select name="type" value={formData.type} onChange={handleChange} className="input">
                                            <option value="Full-time">تمام‌وقت</option>
                                            <option value="Part-time">پاره‌وقت</option>
                                            <option value="Contract">قراردادی</option>
                                            <option value="Freelance">فریلنس</option>
                                        </select>
                                    </div>

                                    <div className="form-group">
                                        <label className="label">سطح تجربه</label>
                                        <select name="experience_level" value={formData.experience_level} onChange={handleChange} className="input">
                                            <option value="Junior">تازه‌کار (۰-۲ سال)</option>
                                            <option value="Mid-Level">میان‌رده (۳-۵ سال)</option>
                                            <option value="Senior">ارشد (۶+ سال)</option>
                                            <option value="Lead">راهبر فنی</option>
                                            <option value="Executive">مدیریتی</option>
                                        </select>
                                    </div>
                                </div>
                            </section>

                            <section>
                                <h2 className="section-title"><List size={18} /> جزئیات و شرح شغل</h2>
                                <div className="space-y-6">
                                    <div className="form-group">
                                        <label className="label">شرح شغل</label>
                                        <textarea
                                            name="description"
                                            value={formData.description}
                                            onChange={handleChange}
                                            rows={6}
                                            className="input py-3 min-h-[150px]"
                                            placeholder="نقش، مسئولیت‌ها و فرهنگ تیمی را به وضوح شرح دهید..."
                                            required
                                        />
                                    </div>

                                    <div className="form-grid">
                                        <div className="form-group">
                                            <label className="label">نیازمندی‌های کلیدی (یک مورد در هر خط)</label>
                                            <textarea
                                                name="requirements"
                                                value={formData.requirements}
                                                onChange={handleChange}
                                                rows={5}
                                                className="input py-3"
                                                placeholder="پایتون&#10;ری‌اکت&#10;معماری ابری AWS&#10;تفکر چابک"
                                            />
                                        </div>

                                        <div className="form-group">
                                            <label className="label">مزایا و تسهیلات (یک مورد در هر خط)</label>
                                            <textarea
                                                name="benefits"
                                                value={formData.benefits}
                                                onChange={handleChange}
                                                rows={5}
                                                className="input py-3"
                                                placeholder="بیمه تکمیلی&#10;ساعت کاری انعطاف‌پذیر&#10;بودجه یادگیری"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </section>

                            <div className="flex flex-col sm:flex-row justify-end gap-4 pt-8 border-t border-slate-100">
                                <button type="button" className="btn btn-secondary px-8 font-semibold" onClick={() => navigate('/dashboard')}>
                                    انصراف
                                </button>
                                <button type="submit" className="btn btn-primary px-12 font-bold shadow-lg shadow-primary/30" disabled={loading}>
                                    {loading ? <span className="loading-dots">در حال انتشار</span> : (
                                        <span className="flex items-center gap-2">
                                            <PlusCircle size={18} /> انتشار آگهی شغلی
                                        </span>
                                    )}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PostJob;
