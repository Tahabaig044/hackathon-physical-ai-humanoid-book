import React from 'react';
import Link from '@docusaurus/Link';

const HeroSection = () => {
  return (
    <div className="hero-section">
      <div className="hero-container">
        <div className="hero-content">
          <h1 className="hero-title">
            Physical AI & Humanoid Robotics
          </h1>
          <p className="hero-subtitle">
            Master the cutting-edge field of embodied artificial intelligence and humanoid robotics.
            Learn from fundamentals to advanced applications with real-world examples and hands-on exercises.
          </p>
          <div className="hero-cta-buttons">
            <Link
              className="button button--primary button--lg hero-button"
              to="/docs/intro">
              Start Learning
            </Link>
            <Link
              className="button button--secondary button--lg hero-button"
              to="/docs/module-0-introduction/embodied-intelligence">
              Ask AI Assistant
            </Link>
          </div>
        </div>
        <div className="hero-animation">
          <div className="ai-robot-placeholder">
            <div className="robot-shape">
              <div className="robot-head">
                <div className="robot-eye left-eye"></div>
                <div className="robot-eye right-eye"></div>
              </div>
              <div className="robot-body">
                <div className="robot-chest-light"></div>
              </div>
              <div className="robot-arms">
                <div className="robot-arm left-arm"></div>
                <div className="robot-arm right-arm"></div>
              </div>
              <div className="robot-legs">
                <div className="robot-leg left-leg"></div>
                <div className="robot-leg right-leg"></div>
              </div>
            </div>
            <div className="robot-glow"></div>
            <div className="robot-scan-line"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeroSection;