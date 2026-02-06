import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock } from 'lucide-react';
import './Auth.css';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (isLoading) return; // Guard clause

        setIsLoading(true);
        setError('');

        try {
            await login(email, password);
            navigate('/dashboard');
        } catch (err) {
            // Check for custom backend errors
            const errorMessage = err.response?.data?.detail || 'Invalid email or password';
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <h2>خوش آمدید</h2>
                <p className="auth-subtitle">وارد حساب کاربری خود شوید</p>

                {error && <div className="auth-error">{error}</div>}

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label>آدرس ایمیل</label>
                        <div className="input-with-icon">
                            <Mail size={20} />
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="example@mail.com"
                                required
                                disabled={isLoading}
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
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••"
                                required
                                disabled={isLoading}
                            />
                        </div>
                    </div>

                    <button type="submit" className="auth-btn" disabled={isLoading}>
                        {isLoading ? 'در حال ورود...' : 'ورود'}
                    </button>
                </form>

                <p className="auth-footer">
                    حساب کاربری ندارید؟ <Link to="/register">ثبت‌نام کنید</Link>
                </p>
            </div>
        </div>
    );
};

export default Login;
