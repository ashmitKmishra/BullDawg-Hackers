import React from 'react'
import './Login.css'

function Login() {
  return (
    <div className="login-container">
      <div className="login-content">
        <div className="login-header">
          <h1 className="brand-title">CoverageCompass</h1>
          <p className="brand-subtitle">Your Guide to Smart Benefits & Financial Wellness</p>
        </div>

        <div className="welcome-section">
          <h2 className="welcome-title">Welcome</h2>
          <p className="welcome-description">
            Navigate your benefits and build financial confidence with our smart assistance platform
          </p>
        </div>

        <div className="features-grid">
          <div className="feature-item">
            <div className="feature-icon">📋</div>
            <h3>Benefits Selection Assistance</h3>
            <p>Smart guidance for health, dental, vision, and group benefits</p>
          </div>
          <div className="feature-item">
            <div className="feature-icon">💰</div>
            <h3>Financial Wellness Education</h3>
            <p>Learn budgeting, savings, and long-term planning fundamentals</p>
          </div>
        </div>

        <div className="login-buttons">
          <button className="login-btn employee-btn">
            <span className="btn-label">Employee Login</span>
            <span className="btn-description">Access your personalized benefits guide</span>
          </button>
          <button className="login-btn hr-btn">
            <span className="btn-label">HR Manager Login</span>
            <span className="btn-description">Manage employee benefits and policies</span>
          </button>
        </div>

        <div className="login-footer">
          <p className="footer-note">For internal use only.</p>
          <p className="footer-copyright"> 2025 Lincoln National Corporation</p>
        </div>
      </div>
    </div>
  )
}

export default Login
