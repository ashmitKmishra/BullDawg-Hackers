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

const slideVariants = {
  enter: (direction) => ({ x: direction > 0 ? 300 : -300, opacity: 0 }),
  center: { x: 0, opacity: 1 },
  exit: (direction) => ({ x: direction < 0 ? 300 : -300, opacity: 0 })
}

export default function Questionnaire() {
  const navigate = useNavigate()
  const [stepIndex, setStepIndex] = useState(0)
  const [direction, setDirection] = useState(0)
  const [answers, setAnswers] = useState({})
  const [completed, setCompleted] = useState(false)

  function handleChange(key, value) {
    setAnswers(prev => ({ ...prev, [key]: value }))
  }

  function next() {
    if (stepIndex < steps.length - 1) {
      setDirection(1)
      setStepIndex(s => s + 1)
    } else {
      finish()
    }
  }

  function back() {
    if (stepIndex === 0) {
      navigate('/signup')
      return
    }
    setDirection(-1)
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
        className="q-container" 
        initial={{ scale: 0.95, opacity: 0 }} 
        animate={{ scale: 1, opacity: 1 }} 
        transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
      >
        {!completed && (
          <div className="q-header">
            <motion.button 
              className="back-btn" 
              onClick={back}
              whileHover={{ scale: 1.05, x: -4 }}
              whileTap={{ scale: 0.95 }}
            >
              ← Back
            </motion.button>
            <div className="progress-section">
              <div className="progress-info">
                <span className="progress-label">Questionnaire</span>
                <motion.span 
                  className="progress-pct"
                  key={progressPct}
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  {progressPct}%
                </motion.span>
              </div>
              <div className="progress-track">
                <motion.div 
                  className="progress-fill" 
                  initial={{ width: 0 }}
                  animate={{ width: `${progressPct}%` }}
                  transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
                />
              </div>
            </div>
          </div>
        )}

        <div className="step-dots">
          {steps.map((s, i) => (
            <motion.div 
              key={s.key} 
              className={`dot ${i === stepIndex ? 'active' : i < stepIndex ? 'done' : ''}`}
              whileHover={{ scale: 1.2 }}
              transition={{ duration: 0.2 }}
            >
              {i < stepIndex ? '✓' : i + 1}
            </motion.div>
          ))}
        </div>

        <AnimatePresence mode="wait" custom={direction}>
          {!completed ? (
            <motion.div 
              key={step.key}
              custom={direction}
              variants={slideVariants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
              className="step-content"
            >
              <div className="step-title">
                <motion.span 
                  className="step-icon"
                  initial={{ scale: 0, rotate: -180 }}
                  animate={{ scale: 1, rotate: 0 }}
                  transition={{ duration: 0.5, delay: 0.1 }}
                >
                  {step.icon}
                </motion.span>
                <h2>{step.title}</h2>
              </div>

              <div className="form-fields">
                {step.fields.map((field, i) => (
                  <motion.div 
                    key={field.key} 
                    className="form-field"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.1 + i * 0.08 }}
                  >
                    <label>{field.label}</label>
                    {field.type === 'select' ? (
                      <select 
                        value={answers[field.key] ?? ''} 
                        onChange={(e) => handleChange(field.key, e.target.value)}
                      >
                        <option value="">Select...</option>
                        {field.options.map(opt => (
                          <option key={opt} value={opt}>{opt}</option>
                        ))}
                      </select>
                    ) : field.type === 'textarea' ? (
                      <textarea
                        value={answers[field.key] ?? ''}
                        onChange={(e) => handleChange(field.key, e.target.value)}
                        placeholder={field.placeholder}
                        rows={3}
                      />
                    ) : (
                      <input
                        type={field.type}
                        value={answers[field.key] ?? ''}
                        onChange={(e) => handleChange(field.key, e.target.value)}
                        placeholder={field.placeholder}
                      />
                    )}
                  </motion.div>
                ))}
              </div>

              <div className="q-actions">
                <motion.button 
                  className="btn-secondary" 
                  onClick={back}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  Back
                </motion.button>
                <motion.button 
                  className="btn-primary" 
                  onClick={next}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {stepIndex < steps.length - 1 ? 'Next →' : 'Finish'}
                </motion.button>
              </div>
            </motion.div>
          ) : (
            <motion.div 
              key="complete"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
              className="completion-view"
            >
              <motion.div 
                className="success-circle"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.5, delay: 0.2, type: 'spring', stiffness: 200 }}
              >
                ✓
              </motion.div>
              <h2>All Set!</h2>
              <p>Thanks — your responses were saved. A backend will use these to generate personalized recommendations.</p>
              <motion.button 
                className="btn-primary"
                onClick={() => navigate('/')}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Back to Home
              </motion.button>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  )
}
