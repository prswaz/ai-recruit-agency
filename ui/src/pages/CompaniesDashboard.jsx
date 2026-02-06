import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';
import {
    Building2, Plus, Edit2, Trash2, Eye, BarChart3, Users,
    TrendingUp, Calendar, MapPin, DollarSign, AlertCircle,
    CheckCircle, Clock, Zap, Briefcase
} from 'lucide-react';
import './Dashboard.css';

const CompaniesDashboard = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [companies, setCompanies] = useState([]);
    const [jobs, setJobs] = useState([]);
    const [stats, setStats] = useState({
        totalJobs: 0,
        activeJobs: 0,
        applications: 0,
        totalViews: 0
    });
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('overview');
    const [selectedCompany, setSelectedCompany] = useState(null);

    useEffect(() => {
        if (user?.role !== 'recruiter') {
            navigate('/');
            return;
        }
        fetchData();
    }, [user, navigate]);

    const fetchData = async () => {
        try {
            const [companiesResp, jobsResp] = await Promise.all([
                api.get('/companies/'),
                api.get('/jobs/')
            ]);

            const recruiterCompanies = companiesResp.data;
            setCompanies(recruiterCompanies);

            if (recruiterCompanies.length > 0) {
                setSelectedCompany(recruiterCompanies[0]);
                const recruiterJobs = jobsResp.data.filter(job =>
                    recruiterCompanies.some(c => c.id === job.company?.id)
                );
                setJobs(recruiterJobs);

                setStats({
                    totalJobs: recruiterJobs.length,
                    activeJobs: recruiterJobs.filter(j => j.is_active).length,
                    applications: recruiterJobs.reduce((acc, job) => acc + (job.applications?.length || 0), 0),
                    totalViews: recruiterJobs.reduce((acc, job) => acc + (job.views || 0), 0)
                });
            }
        } catch (error) {
            console.error("Failed to fetch company data", error);
        } finally {
            setLoading(false);
        }
    };

    const deleteJob = async (jobId) => {
        if (!window.confirm('آیا مطمئن هستید؟')) return;
        try {
            await api.delete(`/jobs/${jobId}/`);
            setJobs(jobs.filter(j => j.id !== jobId));
            fetchData();
        } catch (error) {
            console.error("Failed to delete job", error);
        }
    };

    if (loading) {
        return (
            <div className="flex-center" style={{ height: '80vh' }}>
                <div className="spinner"></div>
            </div>
        );
    }

    if (companies.length === 0) {
        return (
            <div className="page-container flex-center">
                <div className="card p-8 text-center max-w-md">
                    <Building2 size={48} className="mx-auto text-slate-300 mb-4" />
                    <h2 className="text-2xl font-bold mb-2">هیچ شرکتی یافت نشد</h2>
                    <p className="text-secondary mb-6">
                        ابتدا باید یک شرکت ایجاد کنید تا بتوانید آگهی‌های شغلی منتشر کنید.
                    </p>
                    <Link to="/post-job" className="btn btn-primary w-full">
                        ایجاد شرکت و انتشار آگهی
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="page-container companies-dashboard">
            <div className="container">
                <header className="page-header mb-8">
                    <div className="header-text">
                        <h1 className="text-4xl font-extrabold">داشبورد شرکت</h1>
                        <p className="text-secondary text-lg">مدیریت شرکت، آگهی‌ها و درخواست‌های استخدام</p>
                    </div>
                    <Link to="/post-job" className="btn btn-primary flex items-center gap-2">
                        <Plus size={18} /> انتشار آگهی جدید
                    </Link>
                </header>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <div className="card p-6 border-l-4 border-blue-500">
                        <div className="flex items-start justify-between">
                            <div>
                                <p className="text-secondary text-sm font-medium">کل آگهی‌ها</p>
                                <h3 className="text-3xl font-bold text-slate-900 mt-2">{stats.totalJobs}</h3>
                            </div>
                            <div className="p-3 bg-blue-50 rounded-lg">
                                <Briefcase size={24} className="text-blue-500" />
                            </div>
                        </div>
                    </div>

                    <div className="card p-6 border-l-4 border-green-500">
                        <div className="flex items-start justify-between">
                            <div>
                                <p className="text-secondary text-sm font-medium">آگهی‌های فعال</p>
                                <h3 className="text-3xl font-bold text-slate-900 mt-2">{stats.activeJobs}</h3>
                            </div>
                            <div className="p-3 bg-green-50 rounded-lg">
                                <CheckCircle size={24} className="text-green-500" />
                            </div>
                        </div>
                    </div>

                    <div className="card p-6 border-l-4 border-purple-500">
                        <div className="flex items-start justify-between">
                            <div>
                                <p className="text-secondary text-sm font-medium">درخواست‌ها</p>
                                <h3 className="text-3xl font-bold text-slate-900 mt-2">{stats.applications}</h3>
                            </div>
                            <div className="p-3 bg-purple-50 rounded-lg">
                                <Users size={24} className="text-purple-500" />
                            </div>
                        </div>
                    </div>

                    <div className="card p-6 border-l-4 border-orange-500">
                        <div className="flex items-start justify-between">
                            <div>
                                <p className="text-secondary text-sm font-medium">کل بازدیدها</p>
                                <h3 className="text-3xl font-bold text-slate-900 mt-2">{stats.totalViews}</h3>
                            </div>
                            <div className="p-3 bg-orange-50 rounded-lg">
                                <Eye size={24} className="text-orange-500" />
                            </div>
                        </div>
                    </div>
                </div>

                {/* Tabs */}
                <div className="tabs-container mb-8">
                    <button
                        className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
                        onClick={() => setActiveTab('overview')}
                    >
                        نمای کلی
                    </button>
                    <button
                        className={`tab-btn ${activeTab === 'jobs' ? 'active' : ''}`}
                        onClick={() => setActiveTab('jobs')}
                    >
                        آگهی‌های شغلی
                    </button>
                    <button
                        className={`tab-btn ${activeTab === 'companies' ? 'active' : ''}`}
                        onClick={() => setActiveTab('companies')}
                    >
                        شرکت‌های من
                    </button>
                </div>

                {/* Overview Tab */}
                {activeTab === 'overview' && (
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <div className="lg:col-span-2">
                            <div className="card p-6 mb-6">
                                <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                                    <Zap size={20} className="text-amber-500" />
                                    آگهی‌های اخیر
                                </h3>
                                {jobs.length === 0 ? (
                                    <p className="text-secondary text-center py-8">هنوز آگهی منتشر نشده است</p>
                                ) : (
                                    <div className="space-y-4">
                                        {jobs.slice(0, 5).map(job => (
                                            <div key={job.id} className="border border-slate-100 rounded-lg p-4 hover:border-blue-300 hover:bg-blue-50 transition-all">
                                                <div className="flex items-start justify-between">
                                                    <div className="flex-1">
                                                        <h4 className="font-bold text-slate-900">{job.title}</h4>
                                                        <p className="text-secondary text-sm mt-1 flex items-center gap-2">
                                                            <MapPin size={14} /> {job.location || 'نامشخص'}
                                                        </p>
                                                        <div className="flex items-center gap-4 mt-2 text-xs text-secondary">
                                                            <span className="flex items-center gap-1">
                                                                <Calendar size={12} /> {new Date(job.created_at).toLocaleDateString('fa-IR')}
                                                            </span>
                                                            <span className={`px-2 py-1 rounded ${job.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                                                                {job.is_active ? 'فعال' : 'غیرفعال'}
                                                            </span>
                                                        </div>
                                                    </div>
                                                    <div className="flex items-center gap-2">
                                                        <Link to={`/jobs/${job.id}`} className="btn-icon" title="مشاهده">
                                                            <Eye size={18} />
                                                        </Link>
                                                        <Link to={`/job/${job.id}/applications`} className="btn-icon" title="درخواست‌ها">
                                                            <Users size={18} />
                                                        </Link>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>

                        <div>
                            <div className="card p-6">
                                <h3 className="text-lg font-bold mb-4">شرکت‌های من</h3>
                                <div className="space-y-3">
                                    {companies.map(company => (
                                        <button
                                            key={company.id}
                                            onClick={() => setSelectedCompany(company)}
                                            className={`w-full text-right p-4 rounded-lg border-2 transition-all ${
                                                selectedCompany?.id === company.id
                                                    ? 'border-blue-500 bg-blue-50'
                                                    : 'border-slate-100 hover:border-blue-300'
                                            }`}
                                        >
                                            <h4 className="font-bold text-slate-900">{company.name}</h4>
                                            <p className="text-secondary text-xs mt-1">{company.industry || 'صنعت نامشخص'}</p>
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Jobs Tab */}
                {activeTab === 'jobs' && (
                    <div className="card p-6">
                        <div className="flex items-center justify-between mb-6">
                            <h3 className="text-xl font-bold">تمام آگهی‌های شغلی</h3>
                            <Link to="/post-job" className="btn btn-sm btn-primary flex items-center gap-2">
                                <Plus size={16} /> آگهی جدید
                            </Link>
                        </div>

                        {jobs.length === 0 ? (
                            <div className="text-center py-12">
                                <AlertCircle size={48} className="mx-auto text-slate-300 mb-4" />
                                <p className="text-secondary mb-4">هیچ آگهی شغلی منتشر نشده است</p>
                                <Link to="/post-job" className="btn btn-primary inline-flex items-center gap-2">
                                    <Plus size={18} /> انتشار اولین آگهی
                                </Link>
                            </div>
                        ) : (
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead className="bg-slate-50 border-b border-slate-200">
                                        <tr>
                                            <th className="text-right px-4 py-3 font-semibold text-slate-700">عنوان</th>
                                            <th className="text-right px-4 py-3 font-semibold text-slate-700">محل</th>
                                            <th className="text-right px-4 py-3 font-semibold text-slate-700">وضعیت</th>
                                            <th className="text-right px-4 py-3 font-semibold text-slate-700">درخواست‌ها</th>
                                            <th className="text-center px-4 py-3 font-semibold text-slate-700">عملیات</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {jobs.map(job => (
                                            <tr key={job.id} className="border-b border-slate-100 hover:bg-slate-50">
                                                <td className="px-4 py-3">
                                                    <div>
                                                        <p className="font-semibold text-slate-900">{job.title}</p>
                                                        <p className="text-secondary text-xs">{job.company_name}</p>
                                                    </div>
                                                </td>
                                                <td className="px-4 py-3 text-secondary text-sm">{job.location || '-'}</td>
                                                <td className="px-4 py-3">
                                                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
                                                        job.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                                                    }`}>
                                                        {job.is_active ? 'فعال' : 'غیرفعال'}
                                                    </span>
                                                </td>
                                                <td className="px-4 py-3 text-center">
                                                    <span className="inline-block px-3 py-1 bg-blue-50 text-blue-700 rounded text-sm font-medium">
                                                        {job.applications?.length || 0}
                                                    </span>
                                                </td>
                                                <td className="px-4 py-3 text-center space-x-2 flex justify-center gap-2">
                                                    <Link to={`/jobs/${job.id}`} className="btn-icon text-blue-500 hover:text-blue-700" title="نمایش">
                                                        <Eye size={18} />
                                                    </Link>
                                                    <button onClick={() => deleteJob(job.id)} className="btn-icon text-red-500 hover:text-red-700" title="حذف">
                                                        <Trash2 size={18} />
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>
                )}

                {/* Companies Tab */}
                {activeTab === 'companies' && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {companies.map(company => (
                            <div key={company.id} className="card p-6 hover:shadow-lg transition-shadow">
                                <div className="flex items-start justify-between mb-4">
                                    <div className="flex-1">
                                        <h3 className="text-xl font-bold text-slate-900">{company.name}</h3>
                                        <p className="text-secondary text-sm mt-1">{company.industry || 'صنعت نامشخص'}</p>
                                    </div>
                                    <div className="p-3 bg-slate-100 rounded-lg">
                                        <Building2 size={24} className="text-slate-600" />
                                    </div>
                                </div>

                                {company.description && (
                                    <p className="text-secondary text-sm mb-4 line-clamp-2">{company.description}</p>
                                )}

                                <div className="space-y-2 text-sm mb-6">
                                    {company.location && (
                                        <p className="flex items-center gap-2 text-secondary">
                                            <MapPin size={16} /> {company.location}
                                        </p>
                                    )}
                                    {company.website && (
                                        <p className="flex items-center gap-2 text-secondary">
                                            <span className="text-blue-500 hover:underline cursor-pointer">{company.website}</span>
                                        </p>
                                    )}
                                </div>

                                <div className="flex gap-2">
                                    <button className="btn btn-sm btn-secondary flex-1 flex items-center justify-center gap-2">
                                        <Edit2 size={16} /> ویرایش
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default CompaniesDashboard;
