import { useState, useEffect } from 'react';
import './App.css';

const API_URL = 'http://localhost:3001/api';

function App() {
  const [view, setView] = useState('benefits');
  const [benefits, setBenefits] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [employeeBenefits, setEmployeeBenefits] = useState([]);
  const [newBenefit, setNewBenefit] = useState({ name: '', description: '', cost: '' });
  const [newEmployee, setNewEmployee] = useState({ name: '', email: '', department: '' });
  const [enrollment, setEnrollment] = useState({ employee_id: '', benefit_id: '' });

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

  return (
    <div className="app">
      <header>
        <h1>HR Benefits Manager</h1>
        <nav>
          <button onClick={() => setView('benefits')} className={view === 'benefits' ? 'active' : ''}>
            Manage Benefits
          </button>
          <button onClick={() => setView('employees')} className={view === 'employees' ? 'active' : ''}>
            Manage Employees
          </button>
          <button onClick={() => setView('enrollments')} className={view === 'enrollments' ? 'active' : ''}>
            Employee Benefits
          </button>
        </nav>
      </header>

      <main>
        {view === 'benefits' && (
          <div className="section">
            <h2>Benefits Management</h2>
            <form onSubmit={addBenefit} className="form">
              <input
                placeholder="Benefit Name"
                value={newBenefit.name}
                onChange={(e) => setNewBenefit({ ...newBenefit, name: e.target.value })}
                required
              />
              <input
                placeholder="Description"
                value={newBenefit.description}
                onChange={(e) => setNewBenefit({ ...newBenefit, description: e.target.value })}
              />
              <input
                type="number"
                placeholder="Cost"
                value={newBenefit.cost}
                onChange={(e) => setNewBenefit({ ...newBenefit, cost: e.target.value })}
              />
              <button type="submit">Add Benefit</button>
            </form>
            <div className="list">
              {benefits.map(b => (
                <div key={b.id} className="card">
                  <h3>{b.name}</h3>
                  <p>{b.description}</p>
                  <p className="cost">${b.cost}</p>
                  <button onClick={() => deleteBenefit(b.id)} className="delete">Delete</button>
                </div>
              ))}
            </div>
          </div>
        )}

        {view === 'employees' && (
          <div className="section">
            <h2>Employee Management</h2>
            <form onSubmit={addEmployee} className="form">
              <input
                placeholder="Employee Name"
                value={newEmployee.name}
                onChange={(e) => setNewEmployee({ ...newEmployee, name: e.target.value })}
                required
              />
              <input
                type="email"
                placeholder="Email"
                value={newEmployee.email}
                onChange={(e) => setNewEmployee({ ...newEmployee, email: e.target.value })}
              />
              <input
                placeholder="Department"
                value={newEmployee.department}
                onChange={(e) => setNewEmployee({ ...newEmployee, department: e.target.value })}
              />
              <button type="submit">Add Employee</button>
            </form>
            <div className="list">
              {employees.map(e => (
                <div key={e.id} className="card">
                  <h3>{e.name}</h3>
                  <p>{e.email}</p>
                  <p>{e.department}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {view === 'enrollments' && (
          <div className="section">
            <h2>Employee Benefits Enrollment</h2>
            <form onSubmit={enrollEmployee} className="form">
              <select
                value={enrollment.employee_id}
                onChange={(e) => setEnrollment({ ...enrollment, employee_id: e.target.value })}
                required
              >
                <option value="">Select Employee</option>
                {employees.map(e => <option key={e.id} value={e.id}>{e.name}</option>)}
              </select>
              <select
                value={enrollment.benefit_id}
                onChange={(e) => setEnrollment({ ...enrollment, benefit_id: e.target.value })}
                required
              >
                <option value="">Select Benefit</option>
                {benefits.map(b => <option key={b.id} value={b.id}>{b.name}</option>)}
              </select>
              <button type="submit">Enroll Employee</button>
            </form>
            <div className="list">
              {employeeBenefits.map(eb => (
                <div key={eb.id} className="card">
                  <h3>{eb.employee_name}</h3>
                  <p>Benefit: {eb.benefit_name}</p>
                  <p>Enrolled: {eb.enrollment_date}</p>
                  <button onClick={() => removeEnrollment(eb.id)} className="delete">Remove</button>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
