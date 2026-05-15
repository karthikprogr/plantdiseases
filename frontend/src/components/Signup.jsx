import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authService } from '../services/auth';
import './Login.css'; // Reuse login styles

const Signup = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        // Validation
        if (!username.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/)) {
            setError('Invalid email address format. Please enter a valid email.');
            return;
        }

        if (password.length < 6) {
            setError('Password must be at least 6 characters long.');
            return;
        }

        setLoading(true);

        try {
            await authService.signup(username, password);
            alert('Account created successfully! Please login.');
            navigate('/login');
        } catch (err) {
            setError(err.response?.data?.error || 'An error occurred during signup');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page">
            <div className="bg-animation">
                <div className="leaf"></div>
                <div className="leaf"></div>
                <div className="leaf"></div>
                <div className="leaf"></div>
                <div className="leaf"></div>
            </div>

            <div className="login-wrapper">
                <div className="info-panel">
                    <div className="info-content">
                        <div className="logo">🌿</div>
                        <h1>Join Our Community</h1>
                        <p>Create an account to access our AI-powered plant disease detection system and start protecting your plants today.</p>
                    </div>
                </div>

                <div className="form-panel">
                    <div className="form-header">
                        <h2>Create Account</h2>
                        <p>Sign up to get started</p>
                    </div>

                    {error && (
                        <div className="error-message">
                            <i className="fas fa-exclamation-circle"></i> {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit}>
                        <div className="input-group">
                            <i className="fas fa-envelope"></i>
                            <input
                                type="email"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                placeholder="Email Address"
                                required
                                autoComplete="email"
                            />
                        </div>

                        <div className="input-group">
                            <i className="fas fa-lock"></i>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="Password (min. 6 characters)"
                                required
                                autoComplete="new-password"
                            />
                        </div>

                        <button type="submit" className="submit-btn" disabled={loading}>
                            <i className="fas fa-user-plus"></i> {loading ? 'Creating Account...' : 'Sign Up'}
                        </button>
                    </form>

                    <div className="form-links">
                        <p>
                            Already have an account? <Link to="/login">Sign In</Link>
                        </p>
                    </div>
                </div>
            </div>

            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
        </div>
    );
};

export default Signup;
