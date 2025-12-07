import React, { useState } from 'react';
import BrowserOnly from '@docusaurus/BrowserOnly';
import { useLocation } from '@docusaurus/router';

const ModernNavbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isModuleDropdownOpen, setIsModuleDropdownOpen] = useState(false);
  const location = useLocation();

  const modules = [
    { id: 'intro', label: 'Introduction', path: '/docs/intro' },
    { id: 'module0', label: 'Module 0: Embodied Intelligence', path: '/docs/module-0-introduction' },
    { id: 'module1', label: 'Module 1: ROS 2', path: '/docs/module1-ros2' },
    { id: 'module2', label: 'Module 2: Gazebo & Unity', path: '/docs/module2-gazebo-unity' },
    { id: 'module3', label: 'Module 3: NVIDIA Isaac', path: '/docs/module3-nvidia-isaac' },
    { id: 'module4', label: 'Module 4: Vision-Language-Action', path: '/docs/module4-vla' },
    { id: 'module5', label: 'Module 5: Ethics & Safety', path: '/docs/module-5-ethics-safety' },
    { id: 'capstone', label: 'Capstone: Autonomous Humanoid', path: '/docs/capstone' },
  ];

  const toggleTheme = () => {
    if (typeof window !== 'undefined') {
      const currentTheme = localStorage.getItem('theme') || 'light';
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';
      localStorage.setItem('theme', newTheme);
      document.documentElement.setAttribute('data-theme', newTheme);
      window.dispatchEvent(new Event('theme-change'));
    }
  };

  const isActivePath = (path) => {
    return location.pathname.includes(path);
  };

  return (
    <BrowserOnly>
      {() => (
        <nav className="modern-navbar">
          <div className="navbar-container">
            <div className="navbar-brand">
              <a href="/" className="navbar-logo">
                <img src="/img/logo.svg" alt="Physical AI Logo" />
                <span className="navbar-title">Physical AI & Humanoid Robotics</span>
              </a>
            </div>

            <div className={`navbar-menu ${isMenuOpen ? 'active' : ''}`}>
              <div className="navbar-items">
                <div
                  className={`navbar-dropdown ${isModuleDropdownOpen ? 'active' : ''}`}
                  onMouseEnter={() => setIsModuleDropdownOpen(true)}
                  onMouseLeave={() => setIsModuleDropdownOpen(false)}
                >
                  <button
                    className="dropdown-toggle"
                    onClick={() => setIsModuleDropdownOpen(!isModuleDropdownOpen)}
                  >
                    <i className="icon-modules"></i>
                    Modules
                  </button>
                  <div className="dropdown-menu">
                    {modules.map((module) => (
                      <a
                        key={module.id}
                        href={module.path}
                        className={`dropdown-item ${isActivePath(module.path) ? 'active' : ''}`}
                        onClick={() => setIsModuleDropdownOpen(false)}
                      >
                        {module.label}
                      </a>
                    ))}
                  </div>
                </div>

                <a href="/docs/intro" className="navbar-link">
                  <i className="icon-book"></i>
                  Textbook
                </a>

                {/* <a href="/blog" className="navbar-link">
                  <i className="icon-blog"></i>
                  Blog
                </a> */}

                <a href="https://github.com/Tahabaig044/hackathon-physical-ai-humanoid-book" target="_blank" rel="noopener noreferrer" className="navbar-link">
                  <i className="icon-github"></i>
                  GitHub
                </a>

                <button
                  className="theme-toggle"
                  onClick={toggleTheme}
                  title="Toggle theme"
                >
                  <i className="icon-theme"></i>
                </button>
              </div>
            </div>

            <button
              className="navbar-toggle"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              aria-label="Toggle navigation menu"
            >
              <span className="toggle-bar"></span>
              <span className="toggle-bar"></span>
              <span className="toggle-bar"></span>
            </button>
          </div>
        </nav>
      )}
    </BrowserOnly>
  );
};

export default ModernNavbar;