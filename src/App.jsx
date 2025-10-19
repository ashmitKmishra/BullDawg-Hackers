import { useState, useEffect } from 'react';
import './App.css';
import AIChatbot from './components/AIChatbot';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

function App() {
  const [view, setView] = useState('home');
  const [benefits, setBenefits] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [employeeBenefits, setEmployeeBenefits] = useState([]);
  const [newBenefit, setNewBenefit] = useState({ name: '', description: '', cost: '' });
  const [newEmployee, setNewEmployee] = useState({ name: '', email: '', department: '' });
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [showEnrollModal, setShowEnrollModal] = useState(false);
  const [employeeSearch, setEmployeeSearch] = useState('');
  const [benefitSearch, setBenefitSearch] = useState('');
  const [showAddBenefitForm, setShowAddBenefitForm] = useState(false);
  const [showAddEmployeeForm, setShowAddEmployeeForm] = useState(false);
  const [showManagerDropdown, setShowManagerDropdown] = useState(false);
  const [showChatbot, setShowChatbot] = useState(true);
  const [currentStatIndex, setCurrentStatIndex] = useState(0);

  const hrManagerName = "Sarah Johnson";

  useEffect(() => {
    fetchBenefits();
    fetchEmployees();
    fetchEmployeeBenefits();
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showManagerDropdown && !event.target.closest('.hr-manager')) {
        setShowManagerDropdown(false);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [showManagerDropdown]);

  // Rotating statistics
  useEffect(() => {
    if (view === 'home') {
      const interval = setInterval(() => {
        setCurrentStatIndex((prev) => (prev + 1) % 3);
      }, 5000); // Switch stat every 5 seconds
      return () => clearInterval(interval);
    }
  }, [view]);

  const fetchBenefits = async () => {
    const res = await fetch(`${API_URL}/benefits`);
    setBenefits(await res.json());
  };

  const fetchEmployees = async () => {
    const res = await fetch(`${API_URL}/employees`);
    setEmployees(await res.json());
  };

  const fetchEmployeeBenefits = async () => {
    const res = await fetch(`${API_URL}/employee-benefits`);
    setEmployeeBenefits(await res.json());
  };

  const addBenefit = async (e) => {
    e.preventDefault();
    await fetch(`${API_URL}/benefits`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newBenefit)
    });
    setNewBenefit({ name: '', description: '', cost: '' });
    setShowAddBenefitForm(false);
    fetchBenefits();
  };

  const deleteBenefit = async (id) => {
    await fetch(`${API_URL}/benefits/${id}`, { method: 'DELETE' });
    fetchBenefits();
    fetchEmployeeBenefits();
  };

  const addEmployee = async (e) => {
    e.preventDefault();
    await fetch(`${API_URL}/employees`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newEmployee)
    });
    setNewEmployee({ name: '', email: '', department: '' });
    setShowAddEmployeeForm(false);
    fetchEmployees();
  };

  const enrollEmployee = async (benefitId) => {
    if (!selectedEmployee) return;
    
    // Check if employee already has this benefit
    const alreadyEnrolled = employeeBenefits.some(
      eb => eb.employee_id === selectedEmployee.id && eb.benefit_id === benefitId
    );
    
    if (alreadyEnrolled) {
      alert('This employee is already enrolled in this benefit!');
      return;
    }
    
    await fetch(`${API_URL}/employee-benefits`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        employee_id: selectedEmployee.id, 
        benefit_id: benefitId 
      })
    });
    fetchEmployeeBenefits();
    // Don't close the modal - keep it open for multiple selections
  };

  const removeEnrollment = async (id) => {
    await fetch(`${API_URL}/employee-benefits/${id}`, { method: 'DELETE' });
    fetchEmployeeBenefits();
  };

  const getEmployeeBenefits = (employeeId) => {
    return employeeBenefits.filter(eb => eb.employee_id === employeeId);
  };

  const handleEmployeeClick = (employee) => {
    setSelectedEmployee(employee);
  };

  const closeModal = () => {
    setSelectedEmployee(null);
    setShowEnrollModal(false);
  };

  const handleLogout = () => {
    setShowManagerDropdown(false);
    alert('Logging out...');
    // Add your logout logic here
  };

  // Filter employees based on search
  const filteredEmployees = employees.filter(emp => 
    emp.name.toLowerCase().includes(employeeSearch.toLowerCase()) ||
    emp.email.toLowerCase().includes(employeeSearch.toLowerCase()) ||
    (emp.department && emp.department.toLowerCase().includes(employeeSearch.toLowerCase()))
  );

  // Filter benefits based on search
  const filteredBenefits = benefits.filter(ben =>
    ben.name.toLowerCase().includes(benefitSearch.toLowerCase()) ||
    (ben.description && ben.description.toLowerCase().includes(benefitSearch.toLowerCase()))
  );

  // Calculate statistics
  const calculateStats = () => {
    if (employees.length === 0) {
      return {
        avgBenefits: 0,
        mostUsedBenefit: 'N/A',
        avgPaidPerEmployee: 0
      };
    }

    // Average benefits per employee
    const avgBenefits = (employeeBenefits.length / employees.length).toFixed(1);

    // Most used benefit
    const benefitCounts = {};
    employeeBenefits.forEach(eb => {
      benefitCounts[eb.benefit_id] = (benefitCounts[eb.benefit_id] || 0) + 1;
    });

    let mostUsedBenefitId = null;
    let maxCount = 0;
    for (const [benefitId, count] of Object.entries(benefitCounts)) {
      if (count > maxCount) {
        maxCount = count;
        mostUsedBenefitId = benefitId;
      }
    }

    const mostUsedBenefit = mostUsedBenefitId 
      ? benefits.find(b => b.id === parseInt(mostUsedBenefitId))?.name || 'N/A'
      : 'N/A';

    // Average paid per employee
    let totalCost = 0;
    employeeBenefits.forEach(eb => {
      const benefit = benefits.find(b => b.id === eb.benefit_id);
      if (benefit && benefit.cost) {
        totalCost += parseFloat(benefit.cost) || 0;
      }
    });
    const avgPaidPerEmployee = employees.length > 0 
      ? (totalCost / employees.length).toFixed(2) 
      : 0;

    return { avgBenefits, mostUsedBenefit, avgPaidPerEmployee };
  };

  const stats = calculateStats();

  // Format cost display
  const formatCost = (cost) => {
    return cost === 0 || cost === '0' || cost === '0.00' ? 'Price varies' : `$${cost}/month`;
  };

  const handleChatbotAction = (action) => {
    // Actions are handled within the chatbot itself
    // No automatic tab switching
    return;
  };

  return (
    <div className="app-fullscreen">
      {/* Header */}
      <header className="main-header">
        <div className="header-content">
          <h1 className="company-title">CoverageCompass - Management</h1>
          <div 
            className="hr-manager"
            onClick={() => setShowManagerDropdown(!showManagerDropdown)}
          >
            <span className="manager-label">HR Manager:</span>
            <span className="manager-name">{hrManagerName}</span>
            {showManagerDropdown && (
              <div 
                className="manager-dropdown"
                onClick={(e) => e.stopPropagation()}
              >
                <button onClick={handleLogout} className="logout-btn">
                  🚪 Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Navigation */}
      <nav className="main-nav">
        <button 
          onClick={() => setView('home')} 
          className={view === 'home' ? 'nav-btn active' : 'nav-btn'}
        >
          Home
        </button>
        <button 
          onClick={() => setView('benefits')} 
          className={view === 'benefits' ? 'nav-btn active' : 'nav-btn'}
        >
          Manage Benefits and Policies
        </button>
        <button 
          onClick={() => setView('employees')} 
          className={view === 'employees' ? 'nav-btn active' : 'nav-btn'}
        >
          Manage Employees
        </button>
      </nav>

      {/* Main Content */}
      <main className="main-container">
        
        {/* HOME VIEW */}
        {view === 'home' && (
          <div className="home-view">
            {/* Welcome Message */}
            <div className="welcome-section">
              <h2 className="welcome-title">Welcome to your HR Portal</h2>
              <p className="welcome-subtitle">Here's your HR dashboard overview</p>
            </div>

            {/* Statistics Grid */}
            <div className="stats-grid">
              <div className="stat-card-modern">
                <div className="stat-header">Total Employees</div>
                <div className="stat-value">{employees.length}</div>
              </div>
              
              <div className="stat-card-modern">
                <div className="stat-header">Benefits & Policies</div>
                <div className="stat-value">{benefits.length}</div>
              </div>
              
              <div className={`stat-card-modern rotating ${currentStatIndex === 0 ? 'active' : ''}`}>
                <div className="stat-header">Avg Benefits per Employee</div>
                <div className="stat-value">{stats.avgBenefits}</div>
              </div>
              
              <div className={`stat-card-modern rotating ${currentStatIndex === 1 ? 'active' : ''}`}>
                <div className="stat-header">Most Used Benefit</div>
                <div className="stat-value-text">{stats.mostUsedBenefit}</div>
              </div>
              
              <div className={`stat-card-modern rotating ${currentStatIndex === 2 ? 'active' : ''}`}>
                <div className="stat-header">Avg Cost per Employee</div>
                <div className="stat-value">${stats.avgPaidPerEmployee}</div>
                <div className="stat-unit">per month</div>
              </div>
            </div>
          </div>
        )}

        {/* MANAGE BENEFITS VIEW */}
        {view === 'benefits' && (
          <div className="benefits-view">
            <h2 className="page-title">Manage Benefits and Policies</h2>
            
            {!showAddBenefitForm ? (
              <div className="add-button-container">
                <button 
                  onClick={() => setShowAddBenefitForm(true)}
                  className="show-form-btn"
                >
                  + Add New Benefit/Policy
                </button>
              </div>
            ) : (
              <div className="add-section">
                <div className="section-title-row">
                  <h3>Add New Benefit/Policy</h3>
                  <button 
                    onClick={() => {
                      setShowAddBenefitForm(false);
                      setNewBenefit({ name: '', description: '', cost: '' });
                    }}
                    className="cancel-btn"
                  >
                    Cancel
                  </button>
                </div>
                <form onSubmit={addBenefit} className="add-form">
                  <input
                    type="text"
                    placeholder="Benefit/Policy Name"
                    value={newBenefit.name}
                    onChange={(e) => setNewBenefit({ ...newBenefit, name: e.target.value })}
                    required
                  />
                  <input
                    type="text"
                    placeholder="Description"
                    value={newBenefit.description}
                    onChange={(e) => setNewBenefit({ ...newBenefit, description: e.target.value })}
                  />
                  <input
                    type="number"
                    step="0.01"
                    placeholder="Monthly Cost (enter 0 for variable pricing)"
                    value={newBenefit.cost}
                    onChange={(e) => setNewBenefit({ ...newBenefit, cost: e.target.value })}
                  />
                  <button type="submit" className="add-btn">Add Benefit/Policy</button>
                </form>
              </div>
            )}

            <div className="list-section">
              <div className="section-header">
                <h3>Current Benefits & Policies</h3>
                <input
                  type="text"
                  placeholder="Search benefits..."
                  value={benefitSearch}
                  onChange={(e) => setBenefitSearch(e.target.value)}
                  className="search-input"
                />
              </div>
              <div className="items-grid">
                {filteredBenefits.map(b => (
                  <div key={b.id} className="item-card">
                    <h4>{b.name}</h4>
                    <p>{b.description || 'No description'}</p>
                    <p className="cost-tag">{formatCost(b.cost)}</p>
                    <button onClick={() => deleteBenefit(b.id)} className="delete-btn">
                      Delete
                    </button>
                  </div>
                ))}
                {filteredBenefits.length === 0 && (
                  <p className="empty-message">
                    {benefitSearch ? 'No benefits match your search.' : 'No benefits or policies added yet.'}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* MANAGE EMPLOYEES VIEW */}
        {view === 'employees' && (
          <div className="employees-view">
            <h2 className="page-title">Manage Employees</h2>
            
            {!showAddEmployeeForm ? (
              <div className="add-button-container">
                <button 
                  onClick={() => setShowAddEmployeeForm(true)}
                  className="show-form-btn"
                >
                  + Add New Employee
                </button>
              </div>
            ) : (
              <div className="add-section">
                <div className="section-title-row">
                  <h3>Add New Employee</h3>
                  <button 
                    onClick={() => {
                      setShowAddEmployeeForm(false);
                      setNewEmployee({ name: '', email: '', department: '' });
                    }}
                    className="cancel-btn"
                  >
                    Cancel
                  </button>
                </div>
                <form onSubmit={addEmployee} className="add-form">
                  <input
                    type="text"
                    placeholder="Full Name"
                    value={newEmployee.name}
                    onChange={(e) => setNewEmployee({ ...newEmployee, name: e.target.value })}
                    required
                  />
                  <input
                    type="email"
                    placeholder="Email"
                    value={newEmployee.email}
                    onChange={(e) => setNewEmployee({ ...newEmployee, email: e.target.value })}
                    required
                  />
                  <input
                    type="text"
                    placeholder="Department"
                    value={newEmployee.department}
                    onChange={(e) => setNewEmployee({ ...newEmployee, department: e.target.value })}
                  />
                  <button type="submit" className="add-btn">Add Employee</button>
                </form>
              </div>
            )}

            <div className="list-section">
              <div className="section-header">
                <h3>Employee List</h3>
                <input
                  type="text"
                  placeholder="Search employees..."
                  value={employeeSearch}
                  onChange={(e) => setEmployeeSearch(e.target.value)}
                  className="search-input"
                />
              </div>
              <div className="horizontal-scroll">
                {filteredEmployees.map(e => (
                  <div 
                    key={e.id} 
                    className="employee-card"
                    onClick={() => handleEmployeeClick(e)}
                  >
                    <h4>{e.name}</h4>
                    <p>{e.email}</p>
                    <p>{e.department || 'No department'}</p>
                    <p className="benefits-count">
                      {getEmployeeBenefits(e.id).length} benefits enrolled
                    </p>
                    <button 
                      onClick={(event) => {
                        event.stopPropagation();
                        setSelectedEmployee(e);
                        setShowEnrollModal(true);
                      }}
                      className="enroll-btn"
                    >
                      Add Benefits
                    </button>
                  </div>
                ))}
                {filteredEmployees.length === 0 && (
                  <p className="empty-message">
                    {employeeSearch ? 'No employees match your search.' : 'No employees added yet.'}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Employee Details Modal */}
      {selectedEmployee && !showEnrollModal && (
        <div className="modal-backdrop" onClick={closeModal}>
          <div className="modal-box" onClick={(e) => e.stopPropagation()}>
            <button className="close-modal" onClick={closeModal}>×</button>
            <h2>{selectedEmployee.name}</h2>
            <p className="employee-detail">{selectedEmployee.email}</p>
            <p className="employee-detail">{selectedEmployee.department}</p>
            
            <h3 className="modal-section-title">Enrolled Benefits</h3>
            {getEmployeeBenefits(selectedEmployee.id).length > 0 ? (
              <div className="enrolled-benefits">
                {getEmployeeBenefits(selectedEmployee.id).map(eb => (
                  <div key={eb.id} className="benefit-row">
                    <div>
                      <strong>{eb.benefit_name}</strong>
                      <p>Enrolled: {eb.enrollment_date}</p>
                    </div>
                    <button 
                      onClick={() => removeEnrollment(eb.id)} 
                      className="remove-btn"
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <p className="no-benefits">No benefits enrolled</p>
            )}
            
            <button 
              onClick={() => setShowEnrollModal(true)}
              className="add-btn"
              style={{ marginTop: '1rem' }}
            >
              Add More Benefits
            </button>
          </div>
        </div>
      )}

      {/* Enroll Benefits Modal */}
      {showEnrollModal && selectedEmployee && (
        <div className="modal-backdrop" onClick={closeModal}>
          <div className="modal-box" onClick={(e) => e.stopPropagation()}>
            <button className="close-modal" onClick={closeModal}>×</button>
            <h2>Add Benefits to {selectedEmployee.name}</h2>
            
            <div className="benefits-selection">
              {benefits.map(b => {
                const alreadyEnrolled = employeeBenefits.some(
                  eb => eb.employee_id === selectedEmployee.id && eb.benefit_id === b.id
                );
                return (
                  <div key={b.id} className={`benefit-option ${alreadyEnrolled ? 'already-enrolled' : ''}`}>
                    <div>
                      <strong>{b.name}</strong>
                      <p>{b.description}</p>
                      <p className="cost-tag">{formatCost(b.cost)}</p>
                    </div>
                    <button 
                      onClick={() => enrollEmployee(b.id)}
                      className="select-btn"
                      disabled={alreadyEnrolled}
                    >
                      {alreadyEnrolled ? 'Already Enrolled' : 'Select'}
                    </button>
                  </div>
                );
              })}
              {benefits.length === 0 && (
                <p className="empty-message">No benefits available. Add benefits first.</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* AI Chatbot */}
      {showChatbot && (
        <AIChatbot 
          onClose={() => setShowChatbot(false)}
          onAction={handleChatbotAction}
        />
      )}

      {/* AI Assistant Toggle Button */}
      {!showChatbot && (
        <button 
          className="ai-toggle-btn" 
          onClick={() => setShowChatbot(true)}
          title="Open CoverCompass AI"
        >
          <span className="ai-icon">🤖</span>
          <span className="ai-label">CoverCompass AI</span>
        </button>
      )}
    </div>
  );
}

export default App;
