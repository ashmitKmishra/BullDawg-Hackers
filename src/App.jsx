import { useState, useEffect } from 'react';
import './App.css';

const API_URL = 'http://localhost:3001/api';

function App() {
  const [view, setView] = useState('home');
  const [benefits, setBenefits] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [employeeBenefits, setEmployeeBenefits] = useState([]);
  const [newBenefit, setNewBenefit] = useState({ name: '', description: '', cost: '' });
  const [newEmployee, setNewEmployee] = useState({ name: '', email: '', department: '' });
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [showEnrollModal, setShowEnrollModal] = useState(false);

  const hrManagerName = "Sarah Johnson";

  useEffect(() => {
    fetchBenefits();
    fetchEmployees();
    fetchEmployeeBenefits();
  }, []);

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
    fetchEmployees();
  };

  const enrollEmployee = async (benefitId) => {
    if (!selectedEmployee) return;
    await fetch(`${API_URL}/employee-benefits`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        employee_id: selectedEmployee.id, 
        benefit_id: benefitId 
      })
    });
    fetchEmployeeBenefits();
    setShowEnrollModal(false);
    setSelectedEmployee(null);
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

  return (
    <div className="app-fullscreen">
      {/* Header */}
      <header className="main-header">
        <div className="header-content">
          <h1 className="company-title">HR Benefits Management</h1>
          <div className="hr-manager">
            <span className="manager-label">HR Manager:</span>
            <span className="manager-name">{hrManagerName}</span>
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
            <h2 className="page-title">Dashboard Overview</h2>
            <div className="stats-container">
              <div className="stat-box">
                <div className="stat-number">{employees.length}</div>
                <div className="stat-label">Total Employees</div>
              </div>
              <div className="stat-box">
                <div className="stat-number">{benefits.length}</div>
                <div className="stat-label">Benefits & Policies Offered</div>
              </div>
            </div>
          </div>
        )}

        {/* MANAGE BENEFITS VIEW */}
        {view === 'benefits' && (
          <div className="benefits-view">
            <h2 className="page-title">Manage Benefits and Policies</h2>
            
            <div className="add-section">
              <h3>Add New Benefit/Policy</h3>
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
                  placeholder="Monthly Cost"
                  value={newBenefit.cost}
                  onChange={(e) => setNewBenefit({ ...newBenefit, cost: e.target.value })}
                />
                <button type="submit" className="add-btn">Add Benefit/Policy</button>
              </form>
            </div>

            <div className="list-section">
              <h3>Current Benefits & Policies</h3>
              <div className="items-grid">
                {benefits.map(b => (
                  <div key={b.id} className="item-card">
                    <h4>{b.name}</h4>
                    <p>{b.description || 'No description'}</p>
                    <p className="cost-tag">${b.cost}/month</p>
                    <button onClick={() => deleteBenefit(b.id)} className="delete-btn">
                      Delete
                    </button>
                  </div>
                ))}
                {benefits.length === 0 && (
                  <p className="empty-message">No benefits or policies added yet.</p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* MANAGE EMPLOYEES VIEW */}
        {view === 'employees' && (
          <div className="employees-view">
            <h2 className="page-title">Manage Employees</h2>
            
            <div className="add-section">
              <h3>Add New Employee</h3>
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

            <div className="list-section">
              <h3>Employee List</h3>
              <div className="items-grid">
                {employees.map(e => (
                  <div 
                    key={e.id} 
                    className="item-card employee-item"
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
                {employees.length === 0 && (
                  <p className="empty-message">No employees added yet.</p>
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
              {benefits.map(b => (
                <div key={b.id} className="benefit-option">
                  <div>
                    <strong>{b.name}</strong>
                    <p>{b.description}</p>
                    <p className="cost-tag">${b.cost}/month</p>
                  </div>
                  <button 
                    onClick={() => enrollEmployee(b.id)}
                    className="select-btn"
                  >
                    Select
                  </button>
                </div>
              ))}
              {benefits.length === 0 && (
                <p className="empty-message">No benefits available. Add benefits first.</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
