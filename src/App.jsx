import { useState, useEffect } from 'react';
import './App.css';

const API_URL = 'http://localhost:3001/api';

function App() {
  const [view, setView] = useState('dashboard');
  const [benefits, setBenefits] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [employeeBenefits, setEmployeeBenefits] = useState([]);
  const [newBenefit, setNewBenefit] = useState({ name: '', description: '', cost: '' });
  const [newEmployee, setNewEmployee] = useState({ name: '', email: '', department: '' });
  const [enrollment, setEnrollment] = useState({ employee_id: '', benefit_id: '' });
  const [selectedEmployee, setSelectedEmployee] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

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

  const enrollEmployee = async (e) => {
    e.preventDefault();
    await fetch(`${API_URL}/employee-benefits`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(enrollment)
    });
    setEnrollment({ employee_id: '', benefit_id: '' });
    fetchEmployeeBenefits();
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
  };

  // Statistics for dashboard
  const getTotalBenefitsCost = () => {
    return benefits.reduce((sum, b) => sum + (parseFloat(b.cost) || 0), 0).toFixed(2);
  };

  const getEnrollmentCount = () => {
    return employeeBenefits.length;
  };

  const getDepartments = () => {
    const depts = [...new Set(employees.map(e => e.department))];
    return depts.filter(d => d);
  };

  // Filter employees by search
  const filteredEmployees = employees.filter(e => 
    e.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    e.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (e.department && e.department.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="app">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="logo">
          <h2>🏢 HR Portal</h2>
          <p className="subtitle">Benefits Management System</p>
        </div>
        <nav className="sidebar-nav">
          <button 
            onClick={() => setView('dashboard')} 
            className={view === 'dashboard' ? 'active' : ''}
          >
            <span className="icon">📊</span>
            <span>Dashboard</span>
          </button>
          <button 
            onClick={() => setView('employees')} 
            className={view === 'employees' ? 'active' : ''}
          >
            <span className="icon">👥</span>
            <span>Employees</span>
          </button>
          <button 
            onClick={() => setView('benefits')} 
            className={view === 'benefits' ? 'active' : ''}
          >
            <span className="icon">🎁</span>
            <span>Benefits</span>
          </button>
          <button 
            onClick={() => setView('enrollments')} 
            className={view === 'enrollments' ? 'active' : ''}
          >
            <span className="icon">📋</span>
            <span>Enrollments</span>
          </button>
        </nav>
        <div className="sidebar-footer">
          <p>© 2025 BullDawg HR</p>
          <p className="version">v1.0.0</p>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="main-content">
        <header className="top-header">
          <h1>
            {view === 'dashboard' ? 'Dashboard Overview' : 
             view === 'employees' ? 'Employee Management' :
             view === 'benefits' ? 'Benefits Management' : 
             'Enrollment Management'}
          </h1>
          <div className="header-actions">
            <span className="user-badge">👤 Admin</span>
          </div>
        </header>

        <main className="content-area">
          {/* Dashboard View */}
          {view === 'dashboard' && (
            <div className="dashboard">
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-icon">👥</div>
                  <div className="stat-details">
                    <h3>{employees.length}</h3>
                    <p>Total Employees</p>
                  </div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">🎁</div>
                  <div className="stat-details">
                    <h3>{benefits.length}</h3>
                    <p>Available Benefits</p>
                  </div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">📋</div>
                  <div className="stat-details">
                    <h3>{getEnrollmentCount()}</h3>
                    <p>Active Enrollments</p>
                  </div>
                </div>
                <div className="stat-card">
                  <div className="stat-icon">💰</div>
                  <div className="stat-details">
                    <h3>${getTotalBenefitsCost()}</h3>
                    <p>Total Benefits Value</p>
                  </div>
                </div>
              </div>

              <div className="dashboard-content">
                <div className="dashboard-section">
                  <h2>Recent Enrollments</h2>
                  <div className="recent-list">
                    {employeeBenefits.slice(-5).reverse().map(eb => (
                      <div key={eb.id} className="recent-item">
                        <div className="recent-info">
                          <strong>{eb.employee_name}</strong>
                          <span>enrolled in {eb.benefit_name}</span>
                        </div>
                        <span className="recent-date">{eb.enrollment_date}</span>
                      </div>
                    ))}
                    {employeeBenefits.length === 0 && (
                      <p className="no-data">No enrollments yet</p>
                    )}
                  </div>
                </div>

                <div className="dashboard-section">
                  <h2>Quick Actions</h2>
                  <div className="quick-actions">
                    <button className="action-btn" onClick={() => setView('employees')}>
                      <span>➕</span> Add Employee
                    </button>
                    <button className="action-btn" onClick={() => setView('benefits')}>
                      <span>➕</span> Add Benefit
                    </button>
                    <button className="action-btn" onClick={() => setView('enrollments')}>
                      <span>📝</span> Enroll Employee
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Benefits View */}
          {view === 'benefits' && (
            <div className="section">
              <div className="section-header">
                <h2>Benefits Management</h2>
                <p>Manage company benefits and packages</p>
              </div>
              <form onSubmit={addBenefit} className="professional-form">
                <div className="form-group">
                  <label>Benefit Name *</label>
                  <input
                    placeholder="e.g., Health Insurance"
                    value={newBenefit.name}
                    onChange={(e) => setNewBenefit({ ...newBenefit, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Description</label>
                  <input
                    placeholder="Brief description of the benefit"
                    value={newBenefit.description}
                    onChange={(e) => setNewBenefit({ ...newBenefit, description: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Monthly Cost ($)</label>
                  <input
                    type="number"
                    step="0.01"
                    placeholder="0.00"
                    value={newBenefit.cost}
                    onChange={(e) => setNewBenefit({ ...newBenefit, cost: e.target.value })}
                  />
                </div>
                <button type="submit" className="btn-primary">
                  ➕ Add Benefit
                </button>
              </form>
              <div className="cards-grid">
                {benefits.map(b => (
                  <div key={b.id} className="professional-card benefit-card">
                    <div className="card-header">
                      <h3>{b.name}</h3>
                      <span className="badge">${b.cost}/mo</span>
                    </div>
                    <p className="card-description">{b.description || 'No description provided'}</p>
                    <div className="card-footer">
                      <button onClick={() => deleteBenefit(b.id)} className="btn-danger-small">
                        🗑️ Delete
                      </button>
                    </div>
                  </div>
                ))}
                {benefits.length === 0 && (
                  <div className="empty-state">
                    <p>No benefits added yet. Add your first benefit above!</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Employees View */}
          {view === 'employees' && (
            <div className="section">
              <div className="section-header">
                <h2>Employee Directory</h2>
                <div className="search-box">
                  <input 
                    type="text"
                    placeholder="🔍 Search employees..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>
              <form onSubmit={addEmployee} className="professional-form">
                <div className="form-group">
                  <label>Full Name *</label>
                  <input
                    placeholder="e.g., John Doe"
                    value={newEmployee.name}
                    onChange={(e) => setNewEmployee({ ...newEmployee, name: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label>Email Address *</label>
                  <input
                    type="email"
                    placeholder="john.doe@company.com"
                    value={newEmployee.email}
                    onChange={(e) => setNewEmployee({ ...newEmployee, email: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label>Department</label>
                  <input
                    placeholder="e.g., Engineering"
                    value={newEmployee.department}
                    onChange={(e) => setNewEmployee({ ...newEmployee, department: e.target.value })}
                  />
                </div>
                <button type="submit" className="btn-primary">
                  ➕ Add Employee
                </button>
              </form>
              <div className="employee-count">
                Showing {filteredEmployees.length} of {employees.length} employees
              </div>
              <div className="cards-grid">
                {filteredEmployees.map(e => (
                  <div 
                    key={e.id} 
                    className="professional-card employee-card-hover" 
                    onClick={() => handleEmployeeClick(e)}
                  >
                    <div className="employee-avatar">
                      {e.name.charAt(0).toUpperCase()}
                    </div>
                    <div className="employee-info">
                      <h3>{e.name}</h3>
                      <p className="email">📧 {e.email}</p>
                      <p className="department">🏢 {e.department || 'No Department'}</p>
                      <div className="benefit-count">
                        {getEmployeeBenefits(e.id).length} benefits enrolled
                      </div>
                    </div>
                    <div className="card-action">
                      <span className="view-link">View Details →</span>
                    </div>
                  </div>
                ))}
                {filteredEmployees.length === 0 && (
                  <div className="empty-state">
                    <p>{searchTerm ? 'No employees match your search.' : 'No employees added yet.'}</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Enrollments View */}
          {view === 'enrollments' && (
            <div className="section">
              <div className="section-header">
                <h2>Enrollment Management</h2>
                <p>Manage employee benefit enrollments</p>
              </div>
              <form onSubmit={enrollEmployee} className="professional-form enrollment-form">
                <div className="form-group">
                  <label>Select Employee *</label>
                  <select
                    value={enrollment.employee_id}
                    onChange={(e) => setEnrollment({ ...enrollment, employee_id: e.target.value })}
                    required
                  >
                    <option value="">Choose an employee...</option>
                    {employees.map(e => (
                      <option key={e.id} value={e.id}>
                        {e.name} ({e.department || 'No Dept'})
                      </option>
                    ))}
                  </select>
                </div>
                <div className="form-group">
                  <label>Select Benefit *</label>
                  <select
                    value={enrollment.benefit_id}
                    onChange={(e) => setEnrollment({ ...enrollment, benefit_id: e.target.value })}
                    required
                  >
                    <option value="">Choose a benefit...</option>
                    {benefits.map(b => (
                      <option key={b.id} value={b.id}>
                        {b.name} (${b.cost}/mo)
                      </option>
                    ))}
                  </select>
                </div>
                <button type="submit" className="btn-primary">
                  📝 Enroll Employee
                </button>
              </form>
              <div className="enrollments-table">
                <table>
                  <thead>
                    <tr>
                      <th>Employee</th>
                      <th>Benefit</th>
                      <th>Enrollment Date</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {employeeBenefits.map(eb => (
                      <tr key={eb.id}>
                        <td>
                          <strong>{eb.employee_name}</strong>
                          <br />
                          <small>{eb.email}</small>
                        </td>
                        <td>{eb.benefit_name}</td>
                        <td>{eb.enrollment_date}</td>
                        <td>
                          <button 
                            onClick={() => removeEnrollment(eb.id)} 
                            className="btn-danger-small"
                          >
                            Remove
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {employeeBenefits.length === 0 && (
                  <div className="empty-state">
                    <p>No enrollments yet. Start enrolling employees in benefits!</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </main>
      </div>

      {/* Employee Details Modal */}
      {selectedEmployee && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-professional" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={closeModal}>×</button>
            <div className="modal-header">
              <div className="modal-avatar">
                {selectedEmployee.name.charAt(0).toUpperCase()}
              </div>
              <div>
                <h2>{selectedEmployee.name}</h2>
                <p>📧 {selectedEmployee.email}</p>
                <p>🏢 {selectedEmployee.department || 'No Department'}</p>
              </div>
            </div>
            <div className="modal-body">
              <h3>Enrolled Benefits</h3>
              <div className="modal-benefits">
                {getEmployeeBenefits(selectedEmployee.id).length > 0 ? (
                  getEmployeeBenefits(selectedEmployee.id).map(eb => (
                    <div key={eb.id} className="modal-benefit-card">
                      <div className="modal-benefit-info">
                        <h4>{eb.benefit_name}</h4>
                        <p>Enrolled: {eb.enrollment_date}</p>
                      </div>
                      <button 
                        onClick={() => {
                          removeEnrollment(eb.id);
                          closeModal();
                        }} 
                        className="btn-danger-small"
                      >
                        Remove
                      </button>
                    </div>
                  ))
                ) : (
                  <div className="no-benefits-modal">
                    <p>No benefits enrolled yet</p>
                    <button 
                      onClick={() => {
                        closeModal();
                        setView('enrollments');
                      }}
                      className="btn-primary"
                    >
                      Enroll in Benefits
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
