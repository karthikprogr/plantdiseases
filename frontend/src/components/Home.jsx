import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/auth';
import './Home.css';
import './HomePlantsBadge.css';

const Home = () => {
    const navigate = useNavigate();
    const username = authService.getUsername();
    const [selectedPlants, setSelectedPlants] = useState([]);

    // Load selected plants from localStorage
    useEffect(() => {
        const saved = localStorage.getItem('selectedPlants');
        if (saved) {
            setSelectedPlants(JSON.parse(saved));
        }
    }, []);

    const handleLogout = () => {
        authService.logout();
    };

    return (
        <div className="home-page">
            {/* Hero Section */}
            <section className="hero">
                <div className="hero-content">
                    <span className="hero-badge">🌱 AI-Powered Detection</span>
                    <h1>
                        Protect Your Plants with <span className="gradient-text">Smart Technology</span>
                    </h1>
                    <p>
                        Advanced machine learning algorithms detect plant diseases instantly. Upload a photo and get accurate results in seconds.
                    </p>
                    <div className="hero-buttons">
                        <button className="btn-ai" onClick={() => alert('AI Engine coming soon!')}>
                            🔬 Try AI Engine
                        </button>
                        <button className="btn-secondary" onClick={handleLogout}>
                            🚪 Logout
                        </button>
                    </div>
                </div>

                <div className="hero-interactive">
                    {/* Selected Plants Card */}
                    {selectedPlants.length > 0 ? (
                        <div className="interactive-card large">
                            <div className="card-header">
                                <div className="card-icon">🌱</div>
                                <h3 className="card-title">Your Plants ({selectedPlants.length})</h3>
                            </div>
                            <div className="card-content">
                                <div className="selected-plants-list">
                                    {selectedPlants.map((plant) => (
                                        <div key={plant.id} className="plant-badge">
                                            <span className="plant-badge-icon">{plant.icon}</span>
                                            <span className="plant-badge-name">{plant.name}</span>
                                        </div>
                                    ))}
                                </div>
                                <button
                                    className="btn-change-plants"
                                    onClick={() => navigate('/select-plants')}
                                >
                                    ✏️ Change Plants
                                </button>
                            </div>
                        </div>
                    ) : (
                        <div className="interactive-card large">
                            <div className="card-header">
                                <div className="card-icon">🌱</div>
                                <h3 className="card-title">Select Your Plants</h3>
                            </div>
                            <div className="card-content">
                                <p style={{ marginBottom: '1rem', color: 'rgba(255,255,255,0.8)' }}>
                                    Choose the plants you're growing to get personalized disease detection
                                </p>
                                <button
                                    className="btn-change-plants"
                                    onClick={() => navigate('/select-plants')}
                                >
                                    🌿 Select Plants
                                </button>
                            </div>
                        </div>
                    )}

                    <div className="interactive-card">
                        <div className="card-header">
                            <div className="card-icon">🎯</div>
                            <h3 className="card-title">High Accuracy</h3>
                        </div>
                        <div className="card-content">
                            <div className="accuracy-indicator">
                                <div className="accuracy-fill" style={{ width: '95%' }}></div>
                            </div>
                            <p style={{ marginTop: '10px', fontSize: '0.9rem' }}>95% accuracy rate</p>
                        </div>
                    </div>

                    <div className="interactive-card">
                        <div className="card-header">
                            <div className="card-icon">⚡</div>
                            <h3 className="card-title">Fast Results</h3>
                        </div>
                        <div className="card-content">
                            <p style={{ fontSize: '2rem', fontWeight: '700', color: '#50C878' }}>2-5s</p>
                            <p style={{ fontSize: '0.9rem' }}>Average detection time</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Plant Cards Section */}
            <section className="carousel-container">
                <div className="plant-card">
                    <div className="plant-card-inner">
                        <div className="plant-card-front">
                            <div style={{ padding: '20px', textAlign: 'center' }}>
                                <div style={{ fontSize: '4rem' }}>🌿</div>
                                <div className="plant-info">
                                    <p>Tomato</p>
                                </div>
                            </div>
                        </div>
                        <div className="plant-card-back">
                            <p>Detects 10+ tomato diseases including blight, leaf mold, and more</p>
                        </div>
                    </div>
                </div>

                <div className="plant-card">
                    <div className="plant-card-inner">
                        <div className="plant-card-front">
                            <div style={{ padding: '20px', textAlign: 'center' }}>
                                <div style={{ fontSize: '4rem' }}>🥔</div>
                                <div className="plant-info">
                                    <p>Potato</p>
                                </div>
                            </div>
                        </div>
                        <div className="plant-card-back">
                            <p>Identifies early and late blight, leaf diseases</p>
                        </div>
                    </div>
                </div>

                <div className="plant-card">
                    <div className="plant-card-inner">
                        <div className="plant-card-front">
                            <div style={{ padding: '20px', textAlign: 'center' }}>
                                <div style={{ fontSize: '4rem' }}>🌽</div>
                                <div className="plant-info">
                                    <p>Corn</p>
                                </div>
                            </div>
                        </div>
                        <div className="plant-card-back">
                            <p>Detects rust, leaf spot, and other corn diseases</p>
                        </div>
                    </div>
                </div>

                <div className="plant-card">
                    <div className="plant-card-inner">
                        <div className="plant-card-front">
                            <div style={{ padding: '20px', textAlign: 'center' }}>
                                <div style={{ fontSize: '4rem' }}>🍇</div>
                                <div className="plant-info">
                                    <p>Grape</p>
                                </div>
                            </div>
                        </div>
                        <div className="plant-card-back">
                            <p>Identifies black rot, leaf blight, and more</p>
                        </div>
                    </div>
                </div>
            </section>

            <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--text-dark)' }}>
                <p>Welcome, <strong>{username}</strong>! 🎉</p>
            </div>
        </div>
    );
};

export default Home;
