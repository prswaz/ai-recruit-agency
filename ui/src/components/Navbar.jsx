import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogOut, User, Briefcase, FileText, Home, Menu, X } from 'lucide-react';
import './Navbar.css';

const Navbar = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [scrolled, setScrolled] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    // Handle scroll effect
    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const handleLogout = () => {
        logout();
        navigate('/login');
        setMobileMenuOpen(false);
    };

    const isActive = (path) => location.pathname === path ? 'active' : '';

    return (
        <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
            <div className="container navbar-container">
                <Link to="/" className="navbar-logo">
                    <span className="logo-icon">✨</span>
                    <span className="logo-text">استخدام هوشمند</span>
                </Link>

                {/* Desktop Links */}
                <div className="navbar-links desktop-only">
                    {user ? (
                        <>
                            <Link to="/dashboard" className={`nav-link ${isActive('/dashboard')}`}>
                                داشبورد
                            </Link>
                            {user.role === 'candidate' && (
                                <Link to="/analysis-history" className={`nav-link ${isActive('/analysis-history')}`}>
                                    تحلیل‌ها
                                </Link>
                            )}
                            {user.role === 'recruiter' && (
                                <Link to="/post-job" className={`nav-link ${isActive('/post-job')}`}>
                                    ثبت آگهی
                                </Link>
                            )}
                            {user.role === 'candidate' && (
                                <>
                                    <Link to="/jobs" className={`nav-link ${isActive('/jobs')}`}>
                                        فرصت‌های شغلی
                                    </Link>
                                    <Link to="/my-applications" className={`nav-link ${isActive('/my-applications')}`}>
                                        درخواست‌های من
                                    </Link>
                                </>
                            )}

                            <div className="nav-divider"></div>

                            <div className="user-menu">
                                <Link to="/profile" className="profile-link">
                                    <div className="avatar-circle">
                                        {user.first_name?.[0] || user.email[0].toUpperCase()}
                                    </div>
                                    <span className="user-name">{user.first_name || 'کاربر'}</span>
                                </Link>
                                <button onClick={handleLogout} className="btn-icon" title="خروج">
                                    <LogOut size={18} />
                                </button>
                            </div>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="nav-link">ورود</Link>
                            <Link to="/register" className="btn btn-primary">ثبت‌نام</Link>
                        </>
                    )}
                </div>

                {/* Mobile Toggle */}
                <button className="mobile-toggle" onClick={() => setMobileMenuOpen(!mobileMenuOpen)}>
                    {mobileMenuOpen ? <X /> : <Menu />}
                </button>
            </div>

            {/* Mobile Menu */}
            {mobileMenuOpen && (
                <div className="mobile-menu glass-panel">
                    {user ? (
                        <div className="mobile-links">
                            <Link to="/dashboard" onClick={() => setMobileMenuOpen(false)} className="mobile-link">داشبورد</Link>
                            {user.role === 'candidate' && (
                                <>
                                    <Link to="/jobs" onClick={() => setMobileMenuOpen(false)} className="mobile-link">فرصت‌های شغلی</Link>
                                    <Link to="/analysis-history" onClick={() => setMobileMenuOpen(false)} className="mobile-link">تحلیل‌ها</Link>
                                    <Link to="/my-applications" onClick={() => setMobileMenuOpen(false)} className="mobile-link">درخواست‌ها</Link>
                                </>
                            )}
                            {user.role === 'recruiter' && (
                                <Link to="/post-job" onClick={() => setMobileMenuOpen(false)} className="mobile-link">ثبت آگهی</Link>
                            )}
                            <Link to="/profile" onClick={() => setMobileMenuOpen(false)} className="mobile-link">پروفایل</Link>
                            <button onClick={handleLogout} className="mobile-link logout">خروج</button>
                        </div>
                    ) : (
                        <div className="mobile-links">
                            <Link to="/login" onClick={() => setMobileMenuOpen(false)} className="mobile-link">ورود</Link>
                            <Link to="/register" onClick={() => setMobileMenuOpen(false)} className="btn btn-primary w-full">شروع کنید</Link>
                        </div>
                    )}
                </div>
            )}
        </nav>
    );
};

export default Navbar;
