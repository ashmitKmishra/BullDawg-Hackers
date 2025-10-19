import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth0 } from '@auth0/auth0-react'
import './pages.css'

export default function Signup() {
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const navigate = useNavigate()
  const { loginWithRedirect } = useAuth0()

  function handleSubmit(e) {
    e.preventDefault()
    // Kick off Auth0 signup flow and return to questionnaire when done
    loginWithRedirect({
      authorizationParams: {
        screen_hint: 'signup',
        prompt: 'login',
        acr_values: 'http://schemas.openid.net/pape/policies/2007/06/multi-factor',
        scope: 'openid profile email offline_access'
      },
      appState: { returnTo: '/questionnaire' }
    })
  }

  return (
    <div className="page signup">
      <motion.div 
        className="card signup-card" 
        initial={{ y: 20, opacity: 0 }} 
        animate={{ y: 0, opacity: 1 }} 
        transition={{ duration: 0.5 }}
      >
        <div className="signup-top">
          <motion.button 
            className="back" 
            onClick={() => navigate(-1)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            ← Back
          </motion.button>
          <div className="progress-wrap">
            <div className="progress-header">
              <div className="progress-label">Account Setup</div>
              <div className="progress-pct">20%</div>
            </div>
            <div className="progress">
              <motion.div 
                className="progress-bar" 
                initial={{ width: 0 }}
                animate={{ width: '20%' }}
                transition={{ duration: 0.6, ease: 'easeOut' }}
              />
            </div>
          </div>
        </div>

        <form className="form-card" onSubmit={handleSubmit}>
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <h2 style={{ margin: '0 0 0.5rem 0' }}>Create your account</h2>
            <p className="muted">Let's get started with your personalized insurance analysis.</p>
          </motion.div>

          <motion.label
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}
          >
            <span style={{ color: 'var(--muted)', fontWeight: 500 }}>Full name</span>
            <input 
              value={name} 
              onChange={(e) => setName(e.target.value)} 
              placeholder="Jane Doe" 
              required 
            />
          </motion.label>
          
          <motion.label
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}
          >
            <span style={{ color: 'var(--muted)', fontWeight: 500 }}>Email</span>
            <input 
              type="email" 
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
              placeholder="you@example.com" 
              required 
            />
          </motion.label>

          <motion.div
            className="actions"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            style={{ display: 'flex', gap: '0.75rem' }}
          >
            <motion.button 
              type="button" 
              className="ghost" 
              onClick={() => navigate(-1)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Cancel
            </motion.button>
            <motion.button 
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }} 
              className="primary" 
              type="submit"
            >
              Continue with Auth0 →
            </motion.button>
          </motion.div>
        </form>
      </motion.div>
    </div>
  )
}
