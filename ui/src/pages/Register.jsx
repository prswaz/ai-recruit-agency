import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock, User, Briefcase } from 'lucide-react';
import './Auth.css';

const Register = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        role: 'candidate',
        full_name: '',
        company_name: ''
    });
    const [error, setError] = useState('');
    const { register } = useAuth();
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Split full name
            const names = formData.full_name.trim().split(' ');
            const firstName = names[0] || '';
            const lastName = names.slice(1).join(' ') || '';

            const payload = {
                email: formData.email,
                password: formData.password,
                role: formData.role,
                first_name: firstName,
                last_name: lastName
            };

            // If recruiter, we might want to attach company name (but backend serializer doesn't handle it yet in simple register)
            // For now just register the user.

            await register(payload);
            // For now, redirect to login. Could auto-login.
            navigate('/login');
        } catch (err) {
            console.error("Full error object:", err);
            const backendError = err.response?.data;
            let errorMessage = 'Registration failed';

            if (backendError) {
                // Handle different error formats
                if (typeof backendError === 'string') {
                    errorMessage = backendError;
                } else if (backendError.detail) {
                    errorMessage = backendError.detail;
                } else {
                    // Collect all field errors (e.g. email already exists)
                    errorMessage = Object.entries(backendError)
                        .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
                        .join(' | ');
                }
            }

            setError(errorMessage);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <h2>ایجاد حساب کاربری</h2>
                <p className="auth-subtitle">به عنوان کارجو یا کارفرما به ما بپیوندید</p>

                {error && <div className="auth-error">{error}</div>}

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="role-selector">
                        <button
                            type="button"
                            className={`role-btn ${formData.role === 'candidate' ? 'active' : ''}`}
                            onClick={() => setFormData({ ...formData, role: 'candidate' })}
                        >
                            <User size={18} /> داوطلب
                        </button>
                        <button
                            type="button"
                            className={`role-btn ${formData.role === 'recruiter' ? 'active' : ''}`}
                            onClick={() => setFormData({ ...formData, role: 'recruiter' })}
                        >
                            <Briefcase size={18} /> کارفرما
                        </button>
                    </div>

                    <div className="form-group">
                        <label>آدرس ایمیل</label>
                        <div className="input-with-icon">
                            <Mail size={20} />
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                                placeholder="example@mail.com"
                                required
                            />
                        </div>
                    </div>

                    <div className="form-group">
                        <label>رمز عبور</label>
                        <div className="input-with-icon">
                            <Lock size={20} />
                            <input
                                className="input-field"
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                placeholder="••••••••"
                                required
                            />
                        </div>
                    </div>

                    {formData.role === 'candidate' ? (
                        <div className="form-group">
                            <label>نام و نام خانوادگی</label>
                            <div className="input-with-icon">
                                <User size={20} />
                                <input
                                    type="text"
                                    name="full_name"
                                    value={formData.full_name}
                                    onChange={handleChange}
                                    placeholder="نام خود را وارد کنید"
                                    required
                                />
                            </div>
                        </div>
                    ) : (
                        <div className="form-group">
                            <label>نام شرکت</label>
                            <div className="input-with-icon">
                                <Briefcase size={20} />
                                <input
                                    type="text"
                                    name="company_name"
                                    value={formData.company_name}
                                    onChange={handleChange}
                                    placeholder="نام شرکت خود را وارد کنید"
                                    required
                                />
                            </div>
                        </div>
                    )}

                    <button type="submit" className="auth-btn">
                        ایجاد حساب
                    </button>
                </form>

                <p className="auth-footer">
                    قبلاً ثبت‌نام کرده‌اید؟ <Link to="/login">وارد شوید</Link>
                </p>
            </div>
        </div>
    );
};

export default Register;
