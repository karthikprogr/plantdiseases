import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../services/auth';
import './Login.css';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            await authService.login(username, password);
            navigate('/select-plants');
        } catch (err) {
            setError(err.response?.data?.error || 'Invalid username or password');
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleLogin = () => {
        window.location.href = 'http://localhost:5000/api/auth/google-login';
    };

    return (
        <div className="login-page">
            {/* Animated Background */}
            <div className="bg-animation">
                <div className="leaf"></div>
                <div className="leaf"></div>
                <div className="leaf"></div>
                <div className="leaf"></div>
                <div className="leaf"></div>
            </div>

            {/* Main Login Container */}
            <div className="login-wrapper">
                {/* Left Side - Information Panel */}
                <div className="info-panel">
                    <div className="info-content">
                        <div className="logo">🌿</div>
                        <h1>Plant Disease Detection System</h1>
                        <p>Advanced AI-powered plant disease detection to help farmers and gardeners identify and treat plant diseases early.</p>

                        <ul className="features-list">
                            <li>
                                <i className="fas fa-camera"></i>
                                <span>Upload leaf images for instant analysis</span>
                            </li>
                            <li>
                                <i className="fas fa-brain"></i>
                                <span>AI-powered disease classification</span>
                            </li>
                            <li>
                                <i className="fas fa-leaf"></i>
                                <span>Support for 38+ plant diseases</span>
                            </li>
                            <li>
                                <i className="fas fa-chart-line"></i>
                                <span>Real-time prediction & insights</span>
                            </li>
                            <li>
                                <i className="fas fa-mobile-alt"></i>
                                <span>Easy-to-use interface</span>
                            </li>
                        </ul>
                    </div>
                </div>

                {/* Right Side - Login Form */}
                <div className="form-panel">
                    <div className="form-header">
                        <h2>Welcome Back</h2>
                        <p>Sign in to continue to your account</p>
                    </div>

                    {error && (
                        <div className="error-message">
                            <i className="fas fa-exclamation-circle"></i> {error}
                        </div>
                    )}

                    {/* Google Sign-In Button */}
                    <button onClick={handleGoogleLogin} className="google-btn">
                        <svg width="20" height="20" viewBox="0 0 48 48">
                            <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z" />
                            <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z" />
                            <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z" />
                            <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z" />
                        </svg>
                        Continue with Google
                    </button>

                    <div className="divider">
                        <span>OR</span>
                    </div>

                    {/* Login Form */}
                    <form onSubmit={handleSubmit}>
                        <div className="input-group">
                            <i className="fas fa-user"></i>
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Username"
                                required
                                autoComplete="username"
                            />
                        </div>

                        <div className="input-group">
                            <i className="fas fa-lock"></i>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Password"
                                required
                                autoComplete="current-password"
                            />
                        </div>

                        <button type="submit" className="submit-btn" disabled={loading}>
                            <i className="fas fa-sign-in-alt"></i> {loading ? 'Signing in...' : 'Sign In'}
                        </button>
                    </form>

                    <div className="form-links">
                        <p>
                            Don't have an account? <Link to="/signup">Sign Up</Link>
                        </p>
                        <p style={{ marginTop: '10px' }}>
                            <Link to="/forgot-password">Forgot Password?</Link>
                        </p>
                    </div>
                </div>
            </div>

            {/* Font Awesome */}
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
        </div>
    );
};

export default Login;
