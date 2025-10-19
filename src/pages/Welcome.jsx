import { useNavigate } from 'react-router-dom'
import { useAuth0 } from '@auth0/auth0-react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPerson, faUserTie } from '@fortawesome/free-solid-svg-icons'
import './Welcome.css'

const features = [
  {
    title: 'Benefits Selection Assistance',
    description: 'Get personalized recommendations for your health, dental, vision, and group benefits based on your lifestyle and family needs.',
    gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    bgColor: '#ffffff'
  },
  {
    title: 'Financial Wellness Educator',
    description: 'Track your spending, create a personalized budget, and plan for retirement with easy-to-understand guidance.',
    gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    bgColor: '#ffffff'
  }
]

const benefits = [
  { name: 'Dental PPO', description: 'Preferred Provider Organization with access to 125,000+ nationwide providers. Includes MaxRewards® and SmileRewards℠ programs. No referrals required for specialists.', cost: 45.00 },
  { name: 'Dental DHMO', description: 'Dental Health Maintenance Organization with no deductibles, coinsurance, or annual maximums. Available in CA, FL, and TX.', cost: 25.00 },
  { name: 'Dental INO', description: 'In-Network Only plan with nationwide provider access. Available in CA, MD, OH, TN, and DC. No referrals required.', cost: 35.00 },
  { name: 'Self-Funded Dental', description: 'Employer-funded dental plan with administrative services by Lincoln Financial. Customizable plan design.', cost: 0.00 },
  { name: 'Full-Service Eye Plan', description: 'Comprehensive vision coverage including annual exams, frames ($130 allowance), lenses, and contacts ($125 allowance). Includes Children\'s Eye Care Program.', cost: 15.00 },
  { name: 'Lincoln VisionConnect®', description: 'Vision discount program with VSP network access. $50 flat rate eye exams, 15% savings on contact lens exams, special pricing on glasses.', cost: 0.00 },
  { name: 'Term Life Insurance', description: 'Portable life insurance with LifeKeys® legal/financial support, Lincoln FuneralPrep Services, Empathy Beneficiary Services, and TravelConnect®.', cost: 25.00 },
  { name: 'AD&D Insurance', description: 'Accidental Death and Dismemberment coverage providing benefits for accidental death or covered loss such as limb or eyesight.', cost: 8.00 },
  { name: 'Short-Term Disability', description: 'Weekly cash benefit for covered injury, illness, or childbirth. Includes partial benefit for part-time return to work.', cost: 20.00 },
  { name: 'Long-Term Disability', description: 'Monthly income protection for covered injury, illness, or surgery. Includes EmployeeConnect℠ EAP program.', cost: 35.00 },
  { name: 'EmployeeConnect℠ EAP', description: 'Confidential 24/7 support for personal and work/life issues. Up to 5 in-person counseling sessions per person, per issue, per year.', cost: 0.00 },
  { name: 'Accident Insurance', description: 'Direct cash payment for covered injuries and medical services from accidents. Covers ER visits, hospital stays, surgery, fractures, and more.', cost: 12.00 },
  { name: 'Critical Illness Insurance', description: 'Lump-sum cash benefit upon diagnosis of covered critical illness including heart attack, cancer, stroke, renal failure, and organ failure.', cost: 18.00 },
  { name: 'Hospital Indemnity', description: 'Fixed dollar payments for hospital-related events. $1,000 admission, $200/day confinement, $2,000 ICU admission. Includes Health Assessment Benefit.', cost: 15.00 },
  { name: 'TravelConnect®', description: 'Travel assistance service for trips 100+ miles from home. Emergency medical evacuation, repatriation, lost luggage locator, and pre-trip intelligence.', cost: 0.00 },
  { name: 'EPIC Hearing Service', description: 'Discount program with 30-60% off hearing aids, no-cost hearing test, and free battery supply.', cost: 0.00 },
  { name: 'BenefitHub™ Rewards', description: 'Discount marketplace with special pricing on 200+ products and services. Not available in ME, MO, ND, NM, NY, TX, VT, and WA.', cost: 0.00 }
]

export default function Welcome() {
  const navigate = useNavigate()
  const { loginWithRedirect } = useAuth0()

  const handleEmployeeLogin = () => {
    loginWithRedirect({
      authorizationParams: {
        screen_hint: 'signup',
        prompt: 'login',
      },
      appState: { returnTo: '/questionnaire' }
    })
  }

  const handleHRLogin = () => {
    navigate('/dashboard')
  }

  return (
    <div className="welcome-container">
      <div className="welcome-content">
        <header className="welcome-header">
          <h1 className="welcome-title">
            <span className="dollar-icon">💲</span>
            CoverageCompass
          </h1>
          <p className="welcome-subtitle">Your Guide to Smart Benefits Decisions</p>
        </header>

        <div className="login-section">
          <h2 className="section-title">Access Portal</h2>
          <div className="login-buttons">
            <button onClick={handleEmployeeLogin} className="login-btn employee-btn">
              <span className="btn-icon">
                <FontAwesomeIcon icon={faPerson} />
              </span>
              <span className="btn-text">Employee Login</span>
            </button>
            <button onClick={handleHRLogin} className="login-btn hr-btn">
              <span className="btn-icon">
                <FontAwesomeIcon icon={faUserTie} />
              </span>
              <span className="btn-text">HR Login</span>
            </button>
          </div>
        </div>

        <div className="features-section">
          <div className="features-content">
            <h2 className="section-title">Our Services</h2>
            <div className="features-grid">
            {features.map((feature, index) => (
              <div 
                key={index} 
                className="feature-card"
                style={{ backgroundColor: feature.bgColor }}
              >
                <h3 
                  className="feature-title"
                  style={{ background: feature.gradient, WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}
                >
                  {feature.title}
                </h3>
                <p className="feature-description">{feature.description}</p>
              </div>
            ))}
            </div>
          </div>
        </div>

        <div className="benefits-carousel-section">
          <h2 className="section-title">Available Benefits</h2>
          <div className="carousel-container">
            <div className="carousel-track">
              {/* Duplicate benefits array for seamless loop */}
              {[...benefits, ...benefits].map((benefit, index) => (
                <div key={index} className="benefit-card">
                  <h3 className="benefit-name">{benefit.name}</h3>
                  <p className="benefit-description">{benefit.description}</p>
                  <p className="benefit-cost">
                    {benefit.cost === 0 ? 'Free' : `$${benefit.cost.toFixed(2)}/month`}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>

        <footer className="welcome-footer">
          <p>&copy; 2025 CoverageCompass. All rights reserved.</p>
        </footer>
      </div>
    </div>
  )
}
