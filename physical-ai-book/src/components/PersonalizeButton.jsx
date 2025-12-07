import React, { useState, useEffect } from 'react';
import './PersonalizeButton.css';

const PersonalizeButton = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [preferences, setPreferences] = useState({
    experienceLevel: 'intermediate',
    focusArea: 'all',
    notificationEnabled: true
  });

  // Load preferences from localStorage on component mount
  useEffect(() => {
    const savedPreferences = localStorage.getItem('textbookPreferences');
    if (savedPreferences) {
      setPreferences(JSON.parse(savedPreferences));
    }
  }, []);

  // Save preferences to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('textbookPreferences', JSON.stringify(preferences));
  }, [preferences]);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handlePreferenceChange = (key, value) => {
    setPreferences(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const resetPreferences = () => {
    const defaultPrefs = {
      experienceLevel: 'intermediate',
      focusArea: 'all',
      notificationEnabled: true
    };
    setPreferences(defaultPrefs);
    localStorage.setItem('textbookPreferences', JSON.stringify(defaultPrefs));
  };

  return (
    <div className="personalize-container">
      <button
        className="personalize-toggle premium-button"
        onClick={toggleMenu}
        aria-expanded={isOpen}
      >
        <div className="button-content">
          <div className="button-icon">⚙️</div>
          <span className="button-text">Personalize</span>
          <div className="button-arrow">{isOpen ? '▲' : '▼'}</div>
        </div>
      </button>

      {isOpen && (
        <div className="personalize-menu">
          <div className="menu-header">
            <h3>Personalization Settings</h3>
            <button className="menu-close" onClick={toggleMenu} aria-label="Close menu">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              </svg>
            </button>
          </div>

          <div className="preference-group">
            <label className="preference-label">
              <span className="label-icon">🎓</span>
              Experience Level
            </label>
            <select
              value={preferences.experienceLevel}
              onChange={(e) => handlePreferenceChange('experienceLevel', e.target.value)}
              className="preference-select"
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className="preference-group">
            <label className="preference-label">
              <span className="label-icon">🎯</span>
              Focus Area
            </label>
            <select
              value={preferences.focusArea}
              onChange={(e) => handlePreferenceChange('focusArea', e.target.value)}
              className="preference-select"
            >
              <option value="all">All Topics</option>
              <option value="ros2">ROS 2</option>
              <option value="simulation">Simulation</option>
              <option value="nvidia">NVIDIA Isaac</option>
              <option value="vla">Vision-Language-Action</option>
              <option value="humanoid">Humanoid Robotics</option>
            </select>
          </div>

          <div className="preference-group checkbox-group">
            <label className="switch-label">
              <input
                type="checkbox"
                checked={preferences.notificationEnabled}
                onChange={(e) => handlePreferenceChange('notificationEnabled', e.target.checked)}
                className="switch-checkbox"
              />
              <span className="switch-slider"></span>
              <span className="switch-text">Enable content recommendations</span>
            </label>
          </div>

          <div className="preference-actions">
            <button className="reset-btn premium-button secondary" onClick={resetPreferences}>
              <span className="reset-icon">↺</span>
              Reset to Default
            </button>
          </div>

          <p className="preference-info">
            Your preferences help us recommend relevant content and adjust the difficulty level.
          </p>
        </div>
      )}
    </div>
  );
};

export default PersonalizeButton;