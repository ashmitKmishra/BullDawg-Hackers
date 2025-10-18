import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import './pages.css'

export default function Dashboard() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState(null)

  useEffect(() => {
    const userData = sessionStorage.getItem('questionnaire')
    if (!userData) {
      navigate('/questionnaire')
      return
    }
    
    setTimeout(() => {
      setData(JSON.parse(userData))
      setLoading(false)
    }, 2000)
  }, [navigate])

  if (loading) {
    return (
      <div className="page dashboard">
        <motion.div 
          className="loading-container"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <motion.div 
            className="loader"
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          >
            🔄
          </motion.div>
          <h3>Analyzing your data...</h3>
          <p className="muted">Our AI is generating personalized recommendations</p>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="page dashboard">
      <motion.div 
        className="dashboard-container"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="dashboard-header">
          <div>
            <motion.h1
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              Your Insurance Dashboard
            </motion.h1>
            <motion.p 
              className="muted"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              AI-powered insights based on your profile
            </motion.p>
          </div>
          <motion.button 
            className="ghost"
            onClick={() => navigate('/questionnaire')}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
          >
            ← Back to Questionnaire
          </motion.button>
        </div>

        <div className="dashboard-grid">
          {/* Coverage Summary Card */}
          <motion.div 
            className="card dash-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            whileHover={{ y: -4 }}
          >
            <div className="card-header">
              <span className="card-icon">📊</span>
              <h3>Coverage Summary</h3>
            </div>
            <div className="metric-grid">
              <div className="metric">
                <div className="metric-label">Annual Premium</div>
                <div className="metric-value">$4,800</div>
              </div>
              <div className="metric">
                <div className="metric-label">Deductible</div>
                <div className="metric-value">$2,500</div>
              </div>
              <div className="metric">
                <div className="metric-label">Out-of-Pocket Max</div>
                <div className="metric-value">$8,000</div>
              </div>
              <div className="metric">
                <div className="metric-label">Coverage Score</div>
                <div className="metric-value score">78/100</div>
              </div>
            </div>
          </motion.div>

          {/* Recommendations Card */}
          <motion.div 
            className="card dash-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            whileHover={{ y: -4 }}
          >
            <div className="card-header">
              <span className="card-icon">💡</span>
              <h3>Top Recommendations</h3>
            </div>
            <div className="recommendations">
              {[
                { priority: 'High', text: 'Consider adding vision coverage', savings: '$240/year' },
                { priority: 'Medium', text: 'Review dental plan options', savings: '$180/year' },
                { priority: 'Low', text: 'Increase emergency savings', savings: 'Peace of mind' }
              ].map((rec, i) => (
                <motion.div 
                  key={i}
                  className="recommendation"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.5 + i * 0.1 }}
                  whileHover={{ x: 4 }}
                >
                  <span className={`priority ${rec.priority.toLowerCase()}`}>{rec.priority}</span>
                  <div className="rec-content">
                    <div className="rec-text">{rec.text}</div>
                    <div className="rec-savings">{rec.savings}</div>
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Coverage Gaps Card */}
          <motion.div 
            className="card dash-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            whileHover={{ y: -4 }}
          >
            <div className="card-header">
              <span className="card-icon">⚠️</span>
              <h3>Coverage Gaps</h3>
            </div>
            <div className="gaps">
              {[
                { type: 'Vision', status: 'Not Covered', impact: 'Medium' },
                { type: 'Dental', status: 'Basic Only', impact: 'Low' },
                { type: 'Disability', status: 'Not Covered', impact: 'High' }
              ].map((gap, i) => (
                <motion.div 
                  key={i}
                  className="gap-item"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.6 + i * 0.1 }}
                >
                  <div className="gap-type">{gap.type}</div>
                  <div className="gap-status">{gap.status}</div>
                  <span className={`impact ${gap.impact.toLowerCase()}`}>{gap.impact} Impact</span>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Cost Breakdown Chart */}
          <motion.div 
            className="card dash-card chart-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            whileHover={{ y: -4 }}
          >
            <div className="card-header">
              <span className="card-icon">📈</span>
              <h3>Annual Cost Breakdown</h3>
            </div>
            <div className="chart">
              {[
                { label: 'Premiums', value: 4800, color: '#4f46e5', pct: 60 },
                { label: 'Out-of-Pocket', value: 2400, color: '#6ee7b7', pct: 30 },
                { label: 'Uncovered', value: 800, color: '#ef4444', pct: 10 }
              ].map((item, i) => (
                <motion.div 
                  key={i}
                  className="chart-row"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.7 + i * 0.1 }}
                >
                  <div className="chart-label">{item.label}</div>
                  <div className="chart-bar-container">
                    <motion.div 
                      className="chart-bar"
                      style={{ backgroundColor: item.color }}
                      initial={{ width: 0 }}
                      animate={{ width: `${item.pct}%` }}
                      transition={{ delay: 0.8 + i * 0.1, duration: 0.6 }}
                    />
                  </div>
                  <div className="chart-value">${item.value.toLocaleString()}</div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Wellness Tips */}
          <motion.div 
            className="card dash-card"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            whileHover={{ y: -4 }}
          >
            <div className="card-header">
              <span className="card-icon">🏃</span>
              <h3>Wellness Tips</h3>
            </div>
            <div className="tips">
              {[
                'Schedule annual preventive checkup',
                'Review prescription drug coverage',
                'Consider HSA contributions',
                'Update beneficiary information'
              ].map((tip, i) => (
                <motion.div 
                  key={i}
                  className="tip"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.8 + i * 0.08 }}
                  whileHover={{ x: 4 }}
                >
                  <span className="tip-check">✓</span>
                  {tip}
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Action Button */}
          <motion.div 
            className="card dash-card cta-card"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.8 }}
          >
            <h3>Ready to optimize your coverage?</h3>
            <p className="muted">Connect with our AI advisor to get personalized plan recommendations</p>
            <motion.button 
              className="primary large"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => alert('AI Advisor coming soon!')}
            >
              Talk to AI Advisor →
            </motion.button>
          </motion.div>
        </div>
      </motion.div>
    </div>
  )
}
