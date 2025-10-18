// InsuranceChartsPage.jsx - Main page component to display all insurance charts
import { useState, useEffect } from 'react';
import InsurancePremiumChart from './charts/InsurancePremiumChart';
import InsuranceCoverageChart from './charts/InsuranceCoverageChart';
import InsuranceCopayChart from './charts/InsuranceCopayChart';
import InsuranceMaxCoverageChart from './charts/InsuranceMaxCoverageChart';
import insurancePlansData from '../data/insurancePlans.json';

const InsuranceChartsPage = () => {
  const [plans, setPlans] = useState([]);
  const [filteredPlans, setFilteredPlans] = useState([]);
  const [selectedPlan, setSelectedPlan] = useState(null);
  
  // Filter states
  const [premiumRange, setPremiumRange] = useState([0, 1000]);
  const [deductibleRange, setDeductibleRange] = useState([0, 10000]);
  const [copayMax, setCopayMax] = useState(50);
  const [showFamilyCoverage, setShowFamilyCoverage] = useState(null);
  const [chartAnimation, setChartAnimation] = useState(true);

  useEffect(() => {
    // Load insurance plans from JSON
    setPlans(insurancePlansData.insurance_plans);
    setFilteredPlans(insurancePlansData.insurance_plans);
  }, []);

  // Filter plans based on slider values
  useEffect(() => {
    if (plans.length === 0) return;
    
    const filtered = plans.filter(plan => {
      const premiumMatch = plan.premium_monthly >= premiumRange[0] && plan.premium_monthly <= premiumRange[1];
      const deductibleMatch = plan.deductible_annual >= deductibleRange[0] && plan.deductible_annual <= deductibleRange[1];
      const copayMatch = plan.copay_percentage <= copayMax;
      const familyMatch = showFamilyCoverage === null || plan.family_coverage === showFamilyCoverage;
      
      return premiumMatch && deductibleMatch && copayMatch && familyMatch;
    });
    
    setFilteredPlans(filtered);
  }, [premiumRange, deductibleRange, copayMax, showFamilyCoverage, plans]);

  const handlePlanSelect = (planName) => {
    const plan = plans.find(p => p.tier_name === planName);
    setSelectedPlan(plan);
  };

  const resetFilters = () => {
    setPremiumRange([0, 1000]);
    setDeductibleRange([0, 10000]);
    setCopayMax(50);
    setShowFamilyCoverage(null);
  };

  return (
    <div style={{ 
      padding: '2rem',
      maxWidth: '1400px',
      margin: '0 auto',
      background: 'linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%)',
      minHeight: '100vh'
    }}>
      <header style={{ 
        textAlign: 'center', 
        marginBottom: '2rem',
        background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,240,255,0.95) 100%)',
        padding: '2rem',
        borderRadius: '15px',
        boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
        backdropFilter: 'blur(10px)'
      }}>
        <h1 style={{ 
          color: '#1e293b',
          fontSize: '2.5rem',
          marginBottom: '0.5rem',
          textShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          Insurance Plan Comparison Dashboard
        </h1>
        <p style={{ color: '#475569', fontSize: '1.1rem' }}>
          Compare different insurance tiers and find the best plan for you
        </p>
        <p style={{ color: '#7c3aed', fontSize: '0.9rem', marginTop: '0.5rem', fontWeight: 'bold' }}>
          {filteredPlans.length} of {plans.length} plans shown
        </p>
      </header>

      {/* Interactive Controls */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,240,255,0.95) 100%)',
        padding: '2rem',
        borderRadius: '15px',
        boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
        marginBottom: '2rem',
        backdropFilter: 'blur(10px)'
      }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '1.5rem'
        }}>
          <h2 style={{ color: '#1e293b', margin: 0 }}>🎚️ Interactive Filters</h2>
          <button
            onClick={resetFilters}
            style={{
              padding: '0.5rem 1.5rem',
              background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '1rem',
              fontWeight: 'bold',
              transition: 'all 0.3s ease',
              boxShadow: '0 4px 12px rgba(239,68,68,0.4)'
            }}
            onMouseOver={(e) => {
              e.target.style.background = 'linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)';
              e.target.style.transform = 'translateY(-2px)';
              e.target.style.boxShadow = '0 6px 16px rgba(239,68,68,0.5)';
            }}
            onMouseOut={(e) => {
              e.target.style.background = 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)';
              e.target.style.transform = 'translateY(0)';
              e.target.style.boxShadow = '0 4px 12px rgba(239,68,68,0.4)';
            }}
          >
            Reset Filters
          </button>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '1.5rem'
        }}>
          {/* Premium Slider */}
          <div>
            <label style={{ 
              display: 'block', 
              marginBottom: '0.75rem',
              fontWeight: 'bold',
              color: '#555',
              fontSize: '1rem'
            }}>
              💰 Monthly Premium: ${premiumRange[0]} - ${premiumRange[1]}
            </label>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <input
                type="range"
                min="0"
                max="1000"
                value={premiumRange[1]}
                onChange={(e) => setPremiumRange([0, parseInt(e.target.value)])}
                style={{
                  flex: 1,
                  height: '8px',
                  borderRadius: '5px',
                  background: `linear-gradient(to right, #4CAF50 0%, #4CAF50 ${premiumRange[1]/10}%, #ddd ${premiumRange[1]/10}%, #ddd 100%)`,
                  outline: 'none',
                  cursor: 'pointer'
                }}
              />
              <input
                type="number"
                min="0"
                max="1000"
                value={premiumRange[1]}
                onChange={(e) => {
                  const val = Math.min(1000, Math.max(0, parseInt(e.target.value) || 0));
                  setPremiumRange([0, val]);
                }}
                style={{
                  width: '80px',
                  padding: '0.5rem',
                  fontSize: '0.9rem',
                  border: '2px solid #4CAF50',
                  borderRadius: '5px',
                  textAlign: 'center',
                  fontWeight: 'bold'
                }}
              />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#999', marginTop: '0.25rem' }}>
              <span>$0</span>
              <span>$1000</span>
            </div>
          </div>

          {/* Deductible Slider */}
          <div>
            <label style={{ 
              display: 'block', 
              marginBottom: '0.75rem',
              fontWeight: 'bold',
              color: '#555',
              fontSize: '1rem'
            }}>
              🏥 Max Deductible: ${deductibleRange[1].toLocaleString()}
            </label>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <input
                type="range"
                min="0"
                max="10000"
                step="500"
                value={deductibleRange[1]}
                onChange={(e) => setDeductibleRange([0, parseInt(e.target.value)])}
                style={{
                  flex: 1,
                  height: '8px',
                  borderRadius: '5px',
                  background: `linear-gradient(to right, #2196F3 0%, #2196F3 ${deductibleRange[1]/100}%, #ddd ${deductibleRange[1]/100}%, #ddd 100%)`,
                  outline: 'none',
                  cursor: 'pointer'
                }}
              />
              <input
                type="number"
                min="0"
                max="10000"
                step="500"
                value={deductibleRange[1]}
                onChange={(e) => {
                  const val = Math.min(10000, Math.max(0, parseInt(e.target.value) || 0));
                  setDeductibleRange([0, val]);
                }}
                style={{
                  width: '100px',
                  padding: '0.5rem',
                  fontSize: '0.9rem',
                  border: '2px solid #2196F3',
                  borderRadius: '5px',
                  textAlign: 'center',
                  fontWeight: 'bold'
                }}
              />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#999', marginTop: '0.25rem' }}>
              <span>$0</span>
              <span>$10,000</span>
            </div>
          </div>

          {/* Copay Slider */}
          <div>
            <label style={{ 
              display: 'block', 
              marginBottom: '0.75rem',
              fontWeight: 'bold',
              color: '#555',
              fontSize: '1rem'
            }}>
              📊 Max Copay: {copayMax}%
            </label>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <input
                type="range"
                min="0"
                max="50"
                value={copayMax}
                onChange={(e) => setCopayMax(parseInt(e.target.value))}
                style={{
                  flex: 1,
                  height: '8px',
                  borderRadius: '5px',
                  background: `linear-gradient(to right, #FF9800 0%, #FF9800 ${copayMax*2}%, #ddd ${copayMax*2}%, #ddd 100%)`,
                  outline: 'none',
                  cursor: 'pointer'
                }}
              />
              <input
                type="number"
                min="0"
                max="50"
                value={copayMax}
                onChange={(e) => {
                  const val = Math.min(50, Math.max(0, parseInt(e.target.value) || 0));
                  setCopayMax(val);
                }}
                style={{
                  width: '70px',
                  padding: '0.5rem',
                  fontSize: '0.9rem',
                  border: '2px solid #FF9800',
                  borderRadius: '5px',
                  textAlign: 'center',
                  fontWeight: 'bold'
                }}
              />
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#999', marginTop: '0.25rem' }}>
              <span>0%</span>
              <span>50%</span>
            </div>
          </div>

          {/* Family Coverage Toggle */}
          <div>
            <label style={{ 
              display: 'block', 
              marginBottom: '0.75rem',
              fontWeight: 'bold',
              color: '#555',
              fontSize: '1rem'
            }}>
              👨‍👩‍👧‍👦 Family Coverage
            </label>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                onClick={() => setShowFamilyCoverage(null)}
                style={{
                  flex: 1,
                  padding: '0.5rem',
                  background: showFamilyCoverage === null ? 'linear-gradient(135deg, #9333ea 0%, #7e22ce 100%)' : '#e5e7eb',
                  color: showFamilyCoverage === null ? 'white' : '#6b7280',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  transition: 'all 0.3s ease',
                  boxShadow: showFamilyCoverage === null ? '0 4px 12px rgba(147,51,234,0.4)' : 'none'
                }}
              >
                All
              </button>
              <button
                onClick={() => setShowFamilyCoverage(true)}
                style={{
                  flex: 1,
                  padding: '0.5rem',
                  background: showFamilyCoverage === true ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)' : '#e5e7eb',
                  color: showFamilyCoverage === true ? 'white' : '#6b7280',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  transition: 'all 0.3s ease',
                  boxShadow: showFamilyCoverage === true ? '0 4px 12px rgba(16,185,129,0.4)' : 'none'
                }}
              >
                Yes
              </button>
              <button
                onClick={() => setShowFamilyCoverage(false)}
                style={{
                  flex: 1,
                  padding: '0.5rem',
                  background: showFamilyCoverage === false ? 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)' : '#e5e7eb',
                  color: showFamilyCoverage === false ? 'white' : '#6b7280',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  transition: 'all 0.3s ease',
                  boxShadow: showFamilyCoverage === false ? '0 4px 12px rgba(239,68,68,0.4)' : 'none'
                }}
              >
                No
              </button>
            </div>
          </div>
        </div>

        {/* Animation Toggle */}
        <div style={{ marginTop: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <label style={{ fontWeight: 'bold', color: '#1e293b' }}>
            ✨ Chart Animations:
          </label>
          <button
            onClick={() => setChartAnimation(!chartAnimation)}
            style={{
              padding: '0.5rem 1rem',
              background: chartAnimation ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)' : 'linear-gradient(135deg, #6b7280 0%, #4b5563 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '20px',
              cursor: 'pointer',
              fontWeight: 'bold',
              transition: 'all 0.3s ease',
              boxShadow: chartAnimation ? '0 4px 12px rgba(16,185,129,0.4)' : '0 4px 12px rgba(107,114,128,0.4)'
            }}
          >
            {chartAnimation ? 'ON' : 'OFF'}
          </button>
        </div>
      </div>

      {/* Chart Grid */}
      <div style={{ 
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(600px, 1fr))',
        gap: '2rem',
        marginBottom: '2rem'
      }}>
        {/* Premium Chart */}
        <div style={{ 
          background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,240,255,0.95) 100%)',
          padding: '1.5rem',
          borderRadius: '15px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
          transition: 'all 0.3s ease',
          cursor: 'pointer',
          backdropFilter: 'blur(10px)'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.02) translateY(-5px)';
          e.currentTarget.style.boxShadow = '0 12px 48px rgba(0,0,0,0.4)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1) translateY(0)';
          e.currentTarget.style.boxShadow = '0 8px 32px rgba(0,0,0,0.3)';
        }}>
          {filteredPlans.length > 0 && <InsurancePremiumChart plans={filteredPlans} animate={chartAnimation} />}
        </div>

        {/* Coverage Chart */}
        <div style={{ 
          background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,240,255,0.95) 100%)',
          padding: '1.5rem',
          borderRadius: '15px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
          transition: 'all 0.3s ease',
          cursor: 'pointer',
          backdropFilter: 'blur(10px)'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.02) translateY(-5px)';
          e.currentTarget.style.boxShadow = '0 12px 48px rgba(0,0,0,0.4)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1) translateY(0)';
          e.currentTarget.style.boxShadow = '0 8px 32px rgba(0,0,0,0.3)';
        }}>
          {filteredPlans.length > 0 && <InsuranceCoverageChart plans={filteredPlans} animate={chartAnimation} />}
        </div>

        {/* Copay Chart */}
        <div style={{ 
          background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,240,255,0.95) 100%)',
          padding: '1.5rem',
          borderRadius: '15px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
          transition: 'all 0.3s ease',
          cursor: 'pointer',
          backdropFilter: 'blur(10px)'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.02) translateY(-5px) rotateY(5deg)';
          e.currentTarget.style.boxShadow = '0 12px 48px rgba(0,0,0,0.4)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1) translateY(0) rotateY(0deg)';
          e.currentTarget.style.boxShadow = '0 8px 32px rgba(0,0,0,0.3)';
        }}>
          {filteredPlans.length > 0 && <InsuranceCopayChart plans={filteredPlans} animate={chartAnimation} />}
        </div>

        {/* Max Coverage Chart */}
        <div style={{ 
          background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,240,255,0.95) 100%)',
          padding: '1.5rem',
          borderRadius: '15px',
          boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
          transition: 'all 0.3s ease',
          cursor: 'pointer',
          backdropFilter: 'blur(10px)'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.02) translateY(-5px)';
          e.currentTarget.style.boxShadow = '0 12px 48px rgba(0,0,0,0.4)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1) translateY(0)';
          e.currentTarget.style.boxShadow = '0 8px 32px rgba(0,0,0,0.3)';
        }}>
          {filteredPlans.length > 0 && <InsuranceMaxCoverageChart plans={filteredPlans} animate={chartAnimation} />}
        </div>
      </div>

      {/* Plan Details Section */}
      <div style={{ 
        background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,240,255,0.95) 100%)',
        padding: '2rem',
        borderRadius: '15px',
        boxShadow: '0 8px 32px rgba(0,0,0,0.3)',
        marginTop: '2rem',
        backdropFilter: 'blur(10px)'
      }}>
        <h2 style={{ marginBottom: '1.5rem', color: '#1e293b' }}>Plan Details</h2>
        
        {/* Plan Selector */}
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ 
            display: 'block', 
            marginBottom: '0.5rem',
            fontWeight: 'bold',
            color: '#555'
          }}>
            Select a plan to view details:
          </label>
          <select
            onChange={(e) => handlePlanSelect(e.target.value)}
            style={{
              padding: '0.75rem',
              fontSize: '1rem',
              borderRadius: '5px',
              border: '1px solid #ddd',
              width: '100%',
              maxWidth: '400px'
            }}
          >
            <option value="">-- Choose a plan --</option>
            {plans.map(plan => (
              <option key={plan.tier_name} value={plan.tier_name}>
                {plan.tier_name}
              </option>
            ))}
          </select>
        </div>

        {/* Selected Plan Details */}
        {selectedPlan && (
          <div style={{ 
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
            gap: '1.5rem',
            marginTop: '1.5rem'
          }}>
            <div>
              <h3 style={{ color: '#333', marginBottom: '1rem' }}>
                {selectedPlan.tier_name}
              </h3>
              <div style={{ lineHeight: '1.8' }}>
                <p><strong>Monthly Premium:</strong> ${selectedPlan.premium_monthly}</p>
                <p><strong>Annual Deductible:</strong> ${selectedPlan.deductible_annual.toLocaleString()}</p>
                <p><strong>Maximum Coverage:</strong> ${selectedPlan.coverage_max.toLocaleString()}</p>
                <p><strong>Copay Percentage:</strong> {selectedPlan.copay_percentage}%</p>
                <p><strong>Out-of-Pocket Max:</strong> ${selectedPlan.out_of_pocket_max.toLocaleString()}</p>
                <p><strong>Age Range:</strong> {selectedPlan.age_min} - {selectedPlan.age_max}</p>
                <p><strong>Family Coverage:</strong> {selectedPlan.family_coverage ? 'Yes' : 'No'}</p>
                <p><strong>Network Type:</strong> {selectedPlan.network_type}</p>
              </div>
            </div>

            <div>
              <h4 style={{ color: '#2e7d32', marginBottom: '0.75rem' }}>Benefits</h4>
              <ul style={{ lineHeight: '1.8', paddingLeft: '1.5rem' }}>
                {selectedPlan.benefits.map((benefit, index) => (
                  <li key={index}>{benefit}</li>
                ))}
              </ul>
            </div>

            <div>
              <h4 style={{ color: '#c62828', marginBottom: '0.75rem' }}>Exclusions</h4>
              {selectedPlan.exclusions.length > 0 ? (
                <ul style={{ lineHeight: '1.8', paddingLeft: '1.5rem' }}>
                  {selectedPlan.exclusions.map((exclusion, index) => (
                    <li key={index}>{exclusion}</li>
                  ))}
                </ul>
              ) : (
                <p style={{ color: '#666' }}>No exclusions</p>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default InsuranceChartsPage;
