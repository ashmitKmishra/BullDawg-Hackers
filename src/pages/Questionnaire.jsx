import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import './pages.css'

const steps = [
  { id: 1, key: 'personal', title: 'Personal Information', icon: '👤', fields: [
    { key: 'name', label: 'Full Name', type: 'text', placeholder: 'John Doe' },
    { key: 'age', label: 'Age', type: 'number', placeholder: '30' },
    { key: 'gender', label: 'Gender', type: 'select', options: ['Male', 'Female', 'Other', 'Prefer not to say'] }
  ]},
  { id: 2, key: 'family', title: 'Family & Dependents', icon: '👨‍👩‍👧', fields: [
    { key: 'maritalStatus', label: 'Marital Status', type: 'select', options: ['Single', 'Married', 'Divorced', 'Widowed'] },
    { key: 'dependents', label: 'Number of Dependents', type: 'number', placeholder: '0' }
  ]},
  { id: 3, key: 'employment', title: 'Employment & Income', icon: '💼', fields: [
    { key: 'jobType', label: 'Job Type', type: 'select', options: ['Office/Desk', 'Physical Labor', 'Healthcare', 'Education', 'Self-Employed', 'Other'] },
    { key: 'income', label: 'Annual Income (USD)', type: 'number', placeholder: '75000' },
    { key: 'paidTimeOff', label: 'Paid Time Off (days/year)', type: 'number', placeholder: '15' }
  ]},
  { id: 4, key: 'finance', title: 'Financial Health', icon: '💰', fields: [
    { key: 'savings', label: 'Emergency Savings (USD)', type: 'number', placeholder: '10000' },
    { key: 'monthlySpending', label: 'Monthly Spending (USD)', type: 'number', placeholder: '3000' }
  ]},
  { id: 5, key: 'health', title: 'Health & Lifestyle', icon: '❤️', fields: [
    { key: 'preMedicalConditions', label: 'Pre-existing Medical Conditions', type: 'textarea', placeholder: 'List any conditions (optional)' },
    { key: 'lifestyle', label: 'Lifestyle', type: 'select', options: ['Sedentary', 'Moderately Active', 'Very Active', 'Athlete'] },
    { key: 'visionCare', label: 'Need Vision Care?', type: 'select', options: ['Yes', 'No'] },
    { key: 'dentalCare', label: 'Need Dental Care?', type: 'select', options: ['Yes', 'No'] }
  ]}
]

export default function Questionnaire() {
  const navigate = useNavigate()
  const [stepIndex, setStepIndex] = useState(0)
  const [answers, setAnswers] = useState({})
  const [completed, setCompleted] = useState(false)

  function handleChange(key, value) {
    setAnswers(prev => ({ ...prev, [key]: value }))
  }

  function next() {
    if (stepIndex < steps.length - 1) setStepIndex(s => s + 1)
    else finish()
  }

  function back() {
    if (stepIndex === 0) {
      navigate('/signup')
      return
    }
    setStepIndex(s => Math.max(0, s - 1))
  }

  function finish() {
    sessionStorage.setItem('questionnaire', JSON.stringify(answers))
    setCompleted(true)
  }

  const step = steps[stepIndex]
  const progressPct = Math.round(((stepIndex + 1) / steps.length) * 100)

  return (
    <div className="page questionnaire">
      <motion.div 
        className="card q-card" 
        initial={{ y: 20, opacity: 0 }} 
        animate={{ y: 0, opacity: 1 }} 
        transition={{ duration: 0.5 }}
      >
        <div className="signup-top">
          <motion.button 
            className="back" 
            onClick={back}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            ← Back
          </motion.button>
          <div className="progress-wrap">
            <div className="progress-header">
              <div className="progress-label">Questionnaire</div>
              <div className="progress-pct">{progressPct}%</div>
            </div>
            <div className="progress">
              <motion.div 
                className="progress-bar" 
                initial={{ width: 0 }}
                animate={{ width: `${progressPct}%` }}
                transition={{ duration: 0.5, ease: 'easeOut' }}
              />
            </div>
          </div>
        </div>

        <div className="steps-indicator">
          {steps.map((s, i) => (
            <motion.div 
              key={s.key} 
              className={`step-ind ${i === stepIndex ? 'active' : i < stepIndex ? 'done' : ''}`}
              whileHover={{ scale: 1.1 }}
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: i * 0.05 }}
            >
              {i < stepIndex ? '✓' : s.icon}
            </motion.div>
          ))}
        </div>

        <AnimatePresence mode="wait">
          {!completed ? (
            <motion.div 
              key={step.key} 
              initial={{ x: 40, opacity: 0 }} 
              animate={{ x: 0, opacity: 1 }} 
              exit={{ x: -40, opacity: 0 }} 
              transition={{ duration: 0.3 }}
            >
              <div className="step-header">
                <span className="step-icon">{step.icon}</span>
                <h3>{step.title}</h3>
              </div>
              
              <div className="fields">
                {step.fields.map((f, idx) => (
                  <motion.label 
                    key={f.key} 
                    className="field"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.08 }}
                  >
                    {f.label}
                    {f.type === 'select' ? (
                      <select
                        value={answers[f.key] ?? ''}
                        onChange={(e) => handleChange(f.key, e.target.value)}
                      >
                        <option value="">Select...</option>
                        {f.options.map(opt => (
                          <option key={opt} value={opt}>{opt}</option>
                        ))}
                      </select>
                    ) : f.type === 'textarea' ? (
                      <textarea
                        value={answers[f.key] ?? ''}
                        onChange={(e) => handleChange(f.key, e.target.value)}
                        placeholder={f.placeholder}
                        rows={3}
                      />
                    ) : (
                      <input
                        type={f.type}
                        value={answers[f.key] ?? ''}
                        onChange={(e) => handleChange(f.key, e.target.value)}
                        placeholder={f.placeholder}
                      />
                    )}
                  </motion.label>
                ))}
              </div>

              <div className="q-nav">
                <motion.button 
                  onClick={back}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  ← Back
                </motion.button>
                <motion.button 
                  className="primary" 
                  onClick={next}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {stepIndex < steps.length - 1 ? 'Next →' : '✓ Finish'}
                </motion.button>
              </div>
            </motion.div>
          ) : (
            <motion.div 
              key="done" 
              initial={{ scale: 0.9, opacity: 0 }} 
              animate={{ scale: 1, opacity: 1 }} 
              transition={{ duration: 0.5 }}
              className="completion"
            >
              <motion.div 
                className="success-icon"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
              >
                ✓
              </motion.div>
              <h3>All set!</h3>
              <p className="muted">Your responses have been saved. Our AI will analyze your data to generate personalized insurance recommendations.</p>
              <motion.button 
                className="primary view-results"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/dashboard')}
              >
                View My Recommendations →
              </motion.button>
              <details className="debug-details">
                <summary>View submitted data</summary>
                <pre className="debug">{JSON.stringify(answers, null, 2)}</pre>
              </details>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  )
}
