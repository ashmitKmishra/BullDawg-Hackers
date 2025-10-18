import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useState, useEffect } from 'react'
import PhoneGlowSection from '../components/PhoneGlowSection'
import './Welcome.css'


const phoneScreens = [
  {
    title: 'Coverage Summary',
    items: ['📊 Deductibles & Limits', '💰 Out-of-Pocket Max', '🏥 Network Status']
  },
  {
    title: 'Smart Recommendations',
    items: ['✓ Vision Care Needed', '✓ Dental Coverage Gap', '✓ Disability Insurance']
  },
  {
    title: 'Cost Analysis',
    items: ['💵 Monthly Premium', '📈 Savings Potential', '⚡ Quick Wins']
  }
]

const featureCards = [
  {
    icon: '📊',
    title: 'Coverage Summary',
    desc: 'See deductibles, out-of-pocket, and gaps at a glance',
    styles: {
      '--card-background': 'rgba(247, 250, 255, 0.94)',
      '--card-border': 'rgba(37, 99, 235, 0.18)',
      '--card-shadow': '0 24px 50px rgba(37, 99, 235, 0.12)',
      '--card-hover-shadow': '0 32px 70px rgba(37, 99, 235, 0.16)',
      '--card-glow': 'linear-gradient(135deg, rgba(37, 99, 235, 0.35), rgba(59, 130, 246, 0.25))',
      '--icon-background': 'linear-gradient(135deg, rgba(37, 99, 235, 0.18), rgba(59, 130, 246, 0.24))',
      '--icon-shadow': '0 16px 32px rgba(37, 99, 235, 0.18)'
    }
  },
  {
    icon: '🤖',
    title: 'Smart Recommendations',
    desc: 'AI-backed prioritized action items to reduce risk',
    styles: {
      '--card-background': 'rgba(248, 247, 255, 0.94)',
      '--card-border': 'rgba(124, 58, 237, 0.18)',
      '--card-shadow': '0 24px 50px rgba(124, 58, 237, 0.12)',
      '--card-hover-shadow': '0 32px 70px rgba(124, 58, 237, 0.18)',
      '--card-glow': 'linear-gradient(135deg, rgba(124, 58, 237, 0.35), rgba(236, 72, 153, 0.25))',
      '--icon-background': 'linear-gradient(135deg, rgba(124, 58, 237, 0.18), rgba(147, 51, 234, 0.24))',
      '--icon-shadow': '0 16px 32px rgba(124, 58, 237, 0.2)'
    }
  },
  {
    icon: '📈',
    title: 'Charts & Insights',
    desc: 'Beautiful charts that explain tradeoffs and savings',
    styles: {
      '--card-background': 'rgba(241, 252, 255, 0.94)',
      '--card-border': 'rgba(8, 145, 178, 0.18)',
      '--card-shadow': '0 24px 50px rgba(8, 145, 178, 0.12)',
      '--card-hover-shadow': '0 32px 70px rgba(8, 145, 178, 0.18)',
      '--card-glow': 'linear-gradient(135deg, rgba(8, 145, 178, 0.35), rgba(56, 189, 248, 0.25))',
      '--icon-background': 'linear-gradient(135deg, rgba(8, 145, 178, 0.18), rgba(6, 182, 212, 0.24))',
      '--icon-shadow': '0 16px 32px rgba(8, 145, 178, 0.2)'
    }
  },
  {
    icon: '👤',
    title: 'Personalized Analysis',
    desc: 'Tailored to your lifestyle and financial goals',
    styles: {
      '--card-background': 'rgba(241, 253, 249, 0.94)',
      '--card-border': 'rgba(5, 150, 105, 0.18)',
      '--card-shadow': '0 24px 50px rgba(5, 150, 105, 0.12)',
      '--card-hover-shadow': '0 32px 70px rgba(5, 150, 105, 0.18)',
      '--card-glow': 'linear-gradient(135deg, rgba(5, 150, 105, 0.35), rgba(34, 197, 94, 0.25))',
      '--icon-background': 'linear-gradient(135deg, rgba(5, 150, 105, 0.18), rgba(16, 185, 129, 0.24))',
      '--icon-shadow': '0 16px 32px rgba(5, 150, 105, 0.2)'
    }
  }
]

export default function Welcome() {
  const [currentScreen, setCurrentScreen] = useState(0)

  // Cycle through phone screens every 3 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentScreen((prev) => (prev + 1) % phoneScreens.length)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="welcome-page">
      {/* ================================================
          HEADER / NAVBAR - Fixed at top
          ================================================ */}
      <header className="navbar">
        <div className="navbar-container">
          {/* Brand Logo */}
          <div className="brand">
            <span className="brand-icon">🏥</span>
            <span className="brand-name">CoverageCraft</span>
          </div>

          {/* Desktop Navigation */}
          <nav className="nav-links">
            <Link to="/signup" className="nav-link">Get Started</Link>
          </nav>

          {/* Mobile Hamburger Menu */}
          <button className="hamburger" aria-label="Toggle menu">
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </header>

      {/* ================================================
          HERO SECTION - Main welcome content
          Two column layout: text left, phone mockup right
          ================================================ */}
      <main className="hero-section">
        <div className="hero-container">
          {/* LEFT COLUMN - Text Content */}
          <motion.div 
            className="hero-text"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
          >
            {/* Main Headline - Exact wording as requested */}
            <h1 className="hero-headline">
              Claim Smarter,<br />
              Not Harder!
            </h1>

            {/* Subtitle - Exact wording as requested */}
            <p className="hero-subtitle">
            </p>

            {/* CTA Button - With accent color and hover animation */}
            <Link to="/signup">
              <motion.button
                className="cta-button"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.98 }}
              >
                Get Started →
              </motion.button>
            </Link>
          </motion.div>

          {/* RIGHT COLUMN - Phone Mockup with Animated Screens */}
          <motion.div 
            className="hero-image"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
          >
            <div className="phone-container">
              {/* Glow Effect */}
              <motion.div 
                className="phone-glow"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 1, delay: 0.5, ease: "easeOut" }}
              />
              
              <motion.div 
                className="phone-mockup"
                animate={{ 
                  y: [0, -10, 0],
                }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
              >
                {/* Phone Frame - Device mockup container */}
                <div className="phone-frame browser-frame">
                  {/* Browser Window Controls */}
                  <div className="browser-controls">
                    <span className="control-dot red"></span>
                    <span className="control-dot yellow"></span>
                    <span className="control-dot green"></span>
                  </div>
                  
                  {/* Phone Screen Content - App UI preview with animations */}
                  <div className="phone-screen">
                    {/* App Header */}
                    <div className="app-header">
                      <span className="app-logo">🏥 CoverageCraft</span>
                    </div>

                    {/* App Content - Animated Coverage Cards */}
                    <div className="app-content">
                      <motion.div 
                        className="summary-card"
                        key={currentScreen}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        transition={{ duration: 0.5 }}
                      >
                        <h3 className="card-title">{phoneScreens[currentScreen].title}</h3>
                        {phoneScreens[currentScreen].items.map((item, i) => (
                          <motion.div 
                            key={i}
                            className="card-item"
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.4, delay: i * 0.1 }}
                          >
                            {item}
                          </motion.div>
                        ))}
                      </motion.div>

                      {/* Screen Indicator Dots */}
                      <div className="screen-dots">
                        {phoneScreens.map((_, i) => (
                          <motion.div
                            key={i}
                            className={`dot ${i === currentScreen ? 'active' : ''}`}
                            animate={{ scale: i === currentScreen ? 1.2 : 1 }}
                          />
                        ))}
                      </div>

                      {/* Action Button in Phone */}
                      <motion.button 
                        className="phone-button"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                      >
                        CoverageCraft
                      </motion.button>
                    </div>
                  </div>
                </div>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </main>

      {/* ================================================
          FEATURES SECTION - Feature Cards
          ================================================ */}
      <section className="features-section">
        <div className="features-container">
          <motion.h2 
            className="features-heading"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
          >
            Everything you need to make <span className="highlight">smart decisions</span>
          </motion.h2>

          <div className="features-grid">
            {featureCards.map((feature, index) => (
              <motion.div 
                key={feature.title}
                className="feature-card"
                style={feature.styles}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, amount: 0.3 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ 
                  y: -10,
                  transition: { duration: 0.3 }
                }}
              >
                <motion.div 
                  className="feature-icon-wrapper"
                  whileHover={{ 
                    scale: 1.1,
                    rotate: [0, -5, 5, 0]
                  }}
                  transition={{ duration: 0.4 }}
                >
                  <span className="feature-icon">{feature.icon}</span>
                </motion.div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-desc">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
