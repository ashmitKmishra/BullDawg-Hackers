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
      backgroundColor: '#f5f5f5',
      minHeight: '100vh'
    }}>
      <header style={{ 
        textAlign: 'center', 
        marginBottom: '2rem',
        backgroundColor: 'white',
        padding: '2rem',
        borderRadius: '10px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <h1 style={{ 
          color: '#333',
          fontSize: '2.5rem',
          marginBottom: '0.5rem'
        }}>
          Insurance Plan Comparison Dashboard
        </h1>
        <p style={{ color: '#666', fontSize: '1.1rem' }}>
          Compare different insurance tiers and find the best plan for you
        </p>
        <p style={{ color: '#999', fontSize: '0.9rem', marginTop: '0.5rem' }}>
          {filteredPlans.length} of {plans.length} plans shown
        </p>
      </header>

      {/* Interactive Controls */}
      <div style={{
        backgroundColor: 'white',
        padding: '2rem',
        borderRadius: '10px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        marginBottom: '2rem'
      }}>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '1.5rem'
        }}>
          <h2 style={{ color: '#333', margin: 0 }}>🎚️ Interactive Filters</h2>
          <button
            onClick={resetFilters}
            style={{
              padding: '0.5rem 1.5rem',
              backgroundColor: '#ff6b6b',
              color: 'white',
              border: 'none',
              borderRadius: '5px',
              cursor: 'pointer',
              fontSize: '1rem',
              fontWeight: 'bold',
              transition: 'all 0.3s ease'
            }}
            onMouseOver={(e) => e.target.style.backgroundColor = '#ff5252'}
            onMouseOut={(e) => e.target.style.backgroundColor = '#ff6b6b'}
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
            <input
              type="range"
              min="0"
              max="1000"
              value={premiumRange[1]}
              onChange={(e) => setPremiumRange([0, parseInt(e.target.value)])}
              style={{
                width: '100%',
                height: '8px',
                borderRadius: '5px',
                background: `linear-gradient(to right, #4CAF50 0%, #4CAF50 ${premiumRange[1]/10}%, #ddd ${premiumRange[1]/10}%, #ddd 100%)`,
                outline: 'none',
                cursor: 'pointer'
              }}
            />
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
            <input
              type="range"
              min="0"
              max="10000"
              step="500"
              value={deductibleRange[1]}
              onChange={(e) => setDeductibleRange([0, parseInt(e.target.value)])}
              style={{
                width: '100%',
                height: '8px',
                borderRadius: '5px',
                background: `linear-gradient(to right, #2196F3 0%, #2196F3 ${deductibleRange[1]/100}%, #ddd ${deductibleRange[1]/100}%, #ddd 100%)`,
                outline: 'none',
                cursor: 'pointer'
              }}
            />
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
            <input
              type="range"
              min="0"
              max="50"
              value={copayMax}
              onChange={(e) => setCopayMax(parseInt(e.target.value))}
              style={{
                width: '100%',
                height: '8px',
                borderRadius: '5px',
                background: `linear-gradient(to right, #FF9800 0%, #FF9800 ${copayMax*2}%, #ddd ${copayMax*2}%, #ddd 100%)`,
                outline: 'none',
                cursor: 'pointer'
              }}
            />
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
                  backgroundColor: showFamilyCoverage === null ? '#9C27B0' : '#e0e0e0',
                  color: showFamilyCoverage === null ? 'white' : '#666',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  transition: 'all 0.3s ease'
                }}
              >
                All
              </button>
              <button
                onClick={() => setShowFamilyCoverage(true)}
                style={{
                  flex: 1,
                  padding: '0.5rem',
                  backgroundColor: showFamilyCoverage === true ? '#4CAF50' : '#e0e0e0',
                  color: showFamilyCoverage === true ? 'white' : '#666',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  transition: 'all 0.3s ease'
                }}
              >
                Yes
              </button>
              <button
                onClick={() => setShowFamilyCoverage(false)}
                style={{
                  flex: 1,
                  padding: '0.5rem',
                  backgroundColor: showFamilyCoverage === false ? '#f44336' : '#e0e0e0',
                  color: showFamilyCoverage === false ? 'white' : '#666',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  transition: 'all 0.3s ease'
                }}
              >
                No
              </button>
            </div>
          </div>
        </div>

        {/* Animation Toggle */}
        <div style={{ marginTop: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <label style={{ fontWeight: 'bold', color: '#555' }}>
            ✨ Chart Animations:
          </label>
          <button
            onClick={() => setChartAnimation(!chartAnimation)}
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: chartAnimation ? '#4CAF50' : '#9e9e9e',
              color: 'white',
              border: 'none',
              borderRadius: '20px',
              cursor: 'pointer',
              fontWeight: 'bold',
              transition: 'all 0.3s ease'
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
          backgroundColor: 'white',
          padding: '1.5rem',
          borderRadius: '10px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          transition: 'all 0.3s ease',
          cursor: 'pointer'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.02) translateY(-5px)';
          e.currentTarget.style.boxShadow = '0 8px 16px rgba(0,0,0,0.2)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1) translateY(0)';
          e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
        }}>
          {filteredPlans.length > 0 && <InsurancePremiumChart plans={filteredPlans} animate={chartAnimation} />}
        </div>

        {/* Coverage Chart */}
        <div style={{ 
          backgroundColor: 'white',
          padding: '1.5rem',
          borderRadius: '10px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          transition: 'all 0.3s ease',
          cursor: 'pointer'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.02) translateY(-5px)';
          e.currentTarget.style.boxShadow = '0 8px 16px rgba(0,0,0,0.2)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1) translateY(0)';
          e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
        }}>
          {filteredPlans.length > 0 && <InsuranceCoverageChart plans={filteredPlans} animate={chartAnimation} />}
        </div>

        {/* Copay Chart */}
        <div style={{ 
          backgroundColor: 'white',
          padding: '1.5rem',
          borderRadius: '10px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          transition: 'all 0.3s ease',
          cursor: 'pointer'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.02) translateY(-5px) rotateY(5deg)';
          e.currentTarget.style.boxShadow = '0 8px 16px rgba(0,0,0,0.2)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1) translateY(0) rotateY(0deg)';
          e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
        }}>
          {filteredPlans.length > 0 && <InsuranceCopayChart plans={filteredPlans} animate={chartAnimation} />}
        </div>

        {/* Max Coverage Chart */}
        <div style={{ 
          backgroundColor: 'white',
          padding: '1.5rem',
          borderRadius: '10px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          transition: 'all 0.3s ease',
          cursor: 'pointer'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.02) translateY(-5px)';
          e.currentTarget.style.boxShadow = '0 8px 16px rgba(0,0,0,0.2)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1) translateY(0)';
          e.currentTarget.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
        }}>
          {filteredPlans.length > 0 && <InsuranceMaxCoverageChart plans={filteredPlans} animate={chartAnimation} />}
        </div>
      </div>

      {/* Plan Details Section */}
      <div style={{ 
        backgroundColor: 'white',
        padding: '2rem',
        borderRadius: '10px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        marginTop: '2rem'
      }}>
        <h2 style={{ marginBottom: '1.5rem', color: '#333' }}>Plan Details</h2>
        
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
