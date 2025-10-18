// InsuranceChartsPage.jsx - Main page component to display all insurance charts
import { useState, useEffect } from 'react';
import InsurancePremiumChart from './charts/InsurancePremiumChart';
import InsuranceCoverageChart from './charts/InsuranceCoverageChart';
import InsuranceCopayChart from './charts/InsuranceCopayChart';
import InsuranceMaxCoverageChart from './charts/InsuranceMaxCoverageChart';
import insurancePlansData from '../data/insurancePlans.json';

const InsuranceChartsPage = () => {
  const [plans, setPlans] = useState([]);
  const [selectedPlan, setSelectedPlan] = useState(null);

  useEffect(() => {
    // Load insurance plans from JSON
    setPlans(insurancePlansData.insurance_plans);
  }, []);

  const handlePlanSelect = (planName) => {
    const plan = plans.find(p => p.tier_name === planName);
    setSelectedPlan(plan);
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
        marginBottom: '3rem',
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
      </header>

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
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          {plans.length > 0 && <InsurancePremiumChart plans={plans} />}
        </div>

        {/* Coverage Chart */}
        <div style={{ 
          backgroundColor: 'white',
          padding: '1.5rem',
          borderRadius: '10px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          {plans.length > 0 && <InsuranceCoverageChart plans={plans} />}
        </div>

        {/* Copay Chart */}
        <div style={{ 
          backgroundColor: 'white',
          padding: '1.5rem',
          borderRadius: '10px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          {plans.length > 0 && <InsuranceCopayChart plans={plans} />}
        </div>

        {/* Max Coverage Chart */}
        <div style={{ 
          backgroundColor: 'white',
          padding: '1.5rem',
          borderRadius: '10px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          {plans.length > 0 && <InsuranceMaxCoverageChart plans={plans} />}
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
