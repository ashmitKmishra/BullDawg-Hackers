import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import './pages.css'

export default function Welcome() {
  return (
    <div className="page welcome">
      <motion.div 
        className="hero-badge"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        ✨ AI-Powered Insurance Intelligence
      </motion.div>

      <div className="welcome-grid">
        <motion.div 
          className="welcome-left" 
          initial={{ opacity: 0, x: -30 }} 
          animate={{ opacity: 1, x: 0 }} 
          transition={{ duration: 0.7, delay: 0.2 }}
        >
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            CoverageCraft
          </motion.h1>
          
          <motion.p 
            className="tagline"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            Personalized insurance & benefits recommendations — powered by AI, curated for you.
          </motion.p>

          <motion.div 
            className="slogans"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            {[
              { icon: '🎯', text: 'Know your gaps. Close them.' },
              { icon: '💰', text: 'Cut unnecessary spending. Keep the coverage that matters.' },
              { icon: '📊', text: 'Actionable charts, not vague advice.' },
              { icon: '🛡️', text: 'Protect what matters most to you.' }
            ].map((item, i) => (
              <motion.div 
                key={i}
                className="slogan"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 0.6 + i * 0.1 }}
                whileHover={{ scale: 1.02, x: 4 }}
              >
                <span className="slogan-icon">{item.icon}</span>
                {item.text}
              </motion.div>
            ))}
          </motion.div>

          <motion.div 
            className="cta-row"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1 }}
          >
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Link to="/signup" className="cta">Get Started →</Link>
            </motion.div>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <a href="#features" className="ghost">How it works</a>
            </motion.div>
          </motion.div>
        </motion.div>

        <motion.div 
          className="welcome-right" 
          initial={{ opacity: 0, x: 30 }} 
          animate={{ opacity: 1, x: 0 }} 
          transition={{ duration: 0.7, delay: 0.4 }}
        >
          <div className="feature-cards">
            {[
              { title: 'Coverage Summary', desc: 'See deductibles, out-of-pocket, and gaps at a glance.', icon: '📋' },
              { title: 'Smart Recommendations', desc: 'AI-backed prioritized action items to reduce risk and cost.', icon: '🤖' },
              { title: 'Charts & Insights', desc: 'Beautiful charts to explain tradeoffs and savings.', icon: '📈' },
              { title: 'Personalized Analysis', desc: 'Tailored to your lifestyle, family, and financial goals.', icon: '👤' }
            ].map((feature, i) => (
              <motion.div 
                key={i}
                className="feature"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.6 + i * 0.1 }}
                whileHover={{ scale: 1.03, y: -4 }}
              >
                <div className="f-icon">{feature.icon}</div>
                <div className="f-title">{feature.title}</div>
                <div className="f-desc">{feature.desc}</div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}
