import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './PlantSelection.css';

const PlantSelection = () => {
    const navigate = useNavigate();
    const [selectedPlants, setSelectedPlants] = useState([]);
    const [showConfirm, setShowConfirm] = useState(false);

    // Available plants (based on your model's classes)
    const availablePlants = [
        { id: 'apple', name: 'Apple', icon: '🍎', diseases: ['Scab', 'Black Rot', 'Cedar Apple Rust'] },
        { id: 'tomato', name: 'Tomato', icon: '🍅', diseases: ['Bacterial Spot', 'Early Blight', 'Late Blight', 'Leaf Mold', 'Septoria Leaf Spot', 'Spider Mites', 'Target Spot', 'Yellow Leaf Curl Virus', 'Mosaic Virus'] },
        { id: 'potato', name: 'Potato', icon: '🥔', diseases: ['Early Blight', 'Late Blight'] },
        { id: 'corn', name: 'Corn', icon: '🌽', diseases: ['Cercospora Leaf Spot', 'Common Rust', 'Northern Leaf Blight'] },
        { id: 'grape', name: 'Grape', icon: '🍇', diseases: ['Black Rot', 'Esca', 'Leaf Blight'] },
        { id: 'pepper', name: 'Pepper', icon: '🌶️', diseases: ['Bacterial Spot'] },
        { id: 'cherry', name: 'Cherry', icon: '🍒', diseases: ['Powdery Mildew'] },
        { id: 'peach', name: 'Peach', icon: '🍑', diseases: ['Bacterial Spot'] },
        { id: 'strawberry', name: 'Strawberry', icon: '🍓', diseases: ['Leaf Scorch'] },
        { id: 'orange', name: 'Orange', icon: '🍊', diseases: ['Huanglongbing'] },
        { id: 'blueberry', name: 'Blueberry', icon: '🫐', diseases: [] },
        { id: 'raspberry', name: 'Raspberry', icon: '🍇', diseases: [] },
        { id: 'soybean', name: 'Soybean', icon: '🌱', diseases: [] },
        { id: 'squash', name: 'Squash', icon: '🎃', diseases: ['Powdery Mildew'] },
    ];

    // Load saved plants from localStorage
    useEffect(() => {
        const saved = localStorage.getItem('selectedPlants');
        if (saved) {
            setSelectedPlants(JSON.parse(saved));
        }
    }, []);

    const togglePlant = (plant) => {
        if (selectedPlants.find(p => p.id === plant.id)) {
            setSelectedPlants(selectedPlants.filter(p => p.id !== plant.id));
        } else {
            setSelectedPlants([...selectedPlants, plant]);
        }
    };

    const handleContinue = () => {
        if (selectedPlants.length === 0) {
            alert('Please select at least one plant');
            return;
        }

        // Save to localStorage
        localStorage.setItem('selectedPlants', JSON.stringify(selectedPlants));
        setShowConfirm(true);

        // Navigate to home after 1 second
        setTimeout(() => {
            navigate('/home');
        }, 1000);
    };

    const isSelected = (plantId) => {
        return selectedPlants.some(p => p.id === plantId);
    };

    return (
        <div className="plant-selection-page">
            <div className="plant-selection-container">
                <div className="selection-header">
                    <h1>🌿 Select Your Plants</h1>
                    <p>Choose the plants you're growing to get personalized disease detection</p>
                    <div className="selected-count">
                        {selectedPlants.length} plant{selectedPlants.length !== 1 ? 's' : ''} selected
                    </div>
                </div>

                <div className="plants-grid">
                    {availablePlants.map((plant) => (
                        <div
                            key={plant.id}
                            className={`plant-card ${isSelected(plant.id) ? 'selected' : ''}`}
                            onClick={() => togglePlant(plant)}
                        >
                            <div className="plant-icon">{plant.icon}</div>
                            <h3>{plant.name}</h3>
                            <p className="disease-count">
                                {plant.diseases.length > 0
                                    ? `${plant.diseases.length} diseases tracked`
                                    : 'Healthy monitoring'}
                            </p>
                            {isSelected(plant.id) && (
                                <div className="selected-badge">✓</div>
                            )}
                        </div>
                    ))}
                </div>

                <div className="selection-actions">
                    <button className="btn-continue" onClick={handleContinue}>
                        Continue to Dashboard
                    </button>
                    <button className="btn-skip" onClick={() => navigate('/home')}>
                        Skip for now
                    </button>
                </div>

                {showConfirm && (
                    <div className="confirm-overlay">
                        <div className="confirm-message">
                            ✅ Plants saved! Redirecting...
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default PlantSelection;
