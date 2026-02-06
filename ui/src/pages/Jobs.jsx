import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { MapPin, Briefcase, DollarSign, Search, Filter, Building2, Sparkles, ArrowRight } from 'lucide-react';
import './Jobs.css';

const Jobs = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchJobs = async () => {
            try {
                // In a real app, query params would be used for search/filter
                const response = await api.get('/jobs/');
                setJobs(response.data);
            } catch (error) {
                console.error("Error fetching jobs", error);
            } finally {
                setLoading(false);
            }
        };
        fetchJobs();
    }, []);

    const filteredJobs = jobs.filter(job =>
        job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.company_name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (loading) return (
        <div className="flex-center h-screen">
            <div className="spinner"></div>
            <p className="ml-3 text-muted">Loading opportunities...</p>
        </div>
    );

    return (
        <div className="page-container jobs-page">
            <div className="container">
                <div className="jobs-header mb-8 text-center">
                    <div className="badge badge-blue mb-4">
                        <Sparkles size={14} className="mr-2" /> 500+ New Jobs Added Today
                    </div>
                    <h1 className="text-4xl font-bold mb-4">Find Your Dream Job</h1>
                    <p className="text-muted text-lg max-w-2xl mx-auto">
                        Discover role matches based on your unique skills and potential.
                    </p>
                </div>

                {/* Search Bar */}
                <div className="search-bar-container glass-panel mb-12">
                    <div className="search-input-wrapper flex-1">
                        <Search className="search-icon" size={20} />
                        <input
                            type="text"
                            placeholder="Search by job title, company, or keywords..."
                            className="search-input"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <div className="search-divider"></div>
                    <button className="btn btn-secondary filter-btn">
                        <Filter size={18} /> Filters
                    </button>
                    <button className="btn btn-primary px-8">Search</button>
                </div>

                {/* Jobs Grid */}
                <div className="jobs-grid">
                    {filteredJobs.length > 0 ? (
                        filteredJobs.map(job => (
                            <Link to={`/jobs/${job.id}`} key={job.id} className="card job-card hover-lift">
                                <div className="job-card-header mb-4">
                                    <div className="flex justify-between items-start w-full">
                                        {job.logo_url ? (
                                            <img src={job.logo_url} alt={job.company_name} className="company-logo" />
                                        ) : (
                                            <div className="company-logo-placeholder">
                                                <Building2 size={24} />
                                            </div>
                                        )}
                                        {/* Mock Match Badge */}
                                        <div className="match-percent-badge">95% Match</div>
                                    </div>
                                    <div className="job-meta-top mt-2">
                                        <h3 className="job-title">{job.title}</h3>
                                        <div className="company-name">{job.company_name}</div>
                                    </div>
                                </div>

                                <div className="job-tags mb-6">
                                    <span className="tag">
                                        <MapPin size={14} /> {job.location || 'Remote'}
                                    </span>
                                    <span className="tag">
                                        <Briefcase size={14} /> {job.type}
                                    </span>
                                    {job.salary_range && (
                                        <span className="tag tag-green">
                                            <DollarSign size={14} /> {job.salary_range}
                                        </span>
                                    )}
                                </div>

                                <p className="job-description">
                                    {job.description}
                                </p>

                                <div className="job-card-footer mt-auto pt-4 border-t border-light">
                                    <span className="text-sm text-muted">Posted 2 days ago</span>
                                    <span className="details-link group-hover:gap-2 transition-all">
                                        Details <ArrowRight size={16} />
                                    </span>
                                </div>
                            </Link>
                        ))
                    ) : (
                        <div className="col-span-full py-20 px-4 text-center">
                            <div className="w-24 h-24 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-6 text-slate-400">
                                <Search size={40} />
                            </div>
                            <h3 className="text-xl font-bold mb-2 text-main">No opportunities found</h3>
                            <p className="text-muted text-lg max-w-md mx-auto mb-8">
                                We couldn't find any jobs matching "{searchTerm}". Try adjusting your search keywords or filters.
                            </p>
                            <button onClick={() => setSearchTerm('')} className="btn btn-outline text-primary border-primary hover:bg-primary-50">
                                Clear All Search Filters
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Jobs;