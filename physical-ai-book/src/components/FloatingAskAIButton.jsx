import React, { useState, useEffect } from 'react';

const FloatingAskAIButton = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  useEffect(() => {
    // Show button after component mounts with fade-in animation
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, 300);

    return () => clearTimeout(timer);
  }, []);

  const handleClick = () => {
    // Find and open the chat widget if it exists
    const chatButton = document.querySelector('.chat-open-button');
    if (chatButton) {
      chatButton.click();
    } else {
      // If chat widget doesn't exist, redirect to AI section
      window.location.href = '/docs/module-0-introduction/embodied-intelligence';
    }
  };

  return (
    <div
      className={`floating-ask-ai-container ${isVisible ? 'visible' : ''}`}
      style={{
        position: 'fixed',
        bottom: '30px',
        right: '30px',
        zIndex: '1000',
        opacity: isVisible ? 1 : 0,
        transform: isVisible ? 'translateY(0)' : 'translateY(20px)',
        transition: 'opacity 0.3s ease, transform 0.3s ease'
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <button
        className={`floating-ask-ai-button ${isHovered ? 'hovered' : ''}`}
        onClick={handleClick}
        title="Ask AI Assistant"
        aria-label="Ask AI Assistant"
      >
        <div className="ai-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 12 22Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M12 16V12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            <path d="M12 8H12.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
        </div>
        {isHovered && (
          <span className="tooltip">
            Ask AI Assistant
          </span>
        )}
      </button>
    </div>
  );
};

export default FloatingAskAIButton;