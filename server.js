import express from 'express';
import sqlite3 from 'sqlite3';
import cors from 'cors';

const app = express();
const db = new sqlite3.Database('./hr_database.db');

app.use(cors());
app.use(express.json());

// Initialize database
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS benefits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    cost REAL
  )`);

  db.run(`CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    department TEXT
  )`);

  db.run(`CREATE TABLE IF NOT EXISTS employee_benefits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    benefit_id INTEGER,
    enrollment_date TEXT,
    FOREIGN KEY(employee_id) REFERENCES employees(id),
    FOREIGN KEY(benefit_id) REFERENCES benefits(id)
  )`);
});

// Benefits endpoints
app.get('/api/benefits', (req, res) => {
  db.all('SELECT * FROM benefits', [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.post('/api/benefits', (req, res) => {
  const { name, description, cost } = req.body;
  db.run('INSERT INTO benefits (name, description, cost) VALUES (?, ?, ?)', 
    [name, description, cost], function(err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ id: this.lastID, name, description, cost });
    });
});

app.delete('/api/benefits/:id', (req, res) => {
  db.run('DELETE FROM benefits WHERE id = ?', [req.params.id], function(err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ deleted: this.changes });
  });
});

// Employees endpoints
app.get('/api/employees', (req, res) => {
  db.all('SELECT * FROM employees', [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.post('/api/employees', (req, res) => {
  const { name, email, department } = req.body;
  db.run('INSERT INTO employees (name, email, department) VALUES (?, ?, ?)', 
    [name, email, department], function(err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ id: this.lastID, name, email, department });
    });
});

// Employee benefits endpoints
app.get('/api/employee-benefits', (req, res) => {
  const query = `
    SELECT eb.id, e.name as employee_name, e.email, b.name as benefit_name, 
           eb.enrollment_date, e.id as employee_id, b.id as benefit_id
    FROM employee_benefits eb
    JOIN employees e ON eb.employee_id = e.id
    JOIN benefits b ON eb.benefit_id = b.id
  `;
  db.all(query, [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.post('/api/employee-benefits', (req, res) => {
  const { employee_id, benefit_id } = req.body;
  const enrollment_date = new Date().toISOString().split('T')[0];
  db.run('INSERT INTO employee_benefits (employee_id, benefit_id, enrollment_date) VALUES (?, ?, ?)', 
    [employee_id, benefit_id, enrollment_date], function(err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ id: this.lastID, employee_id, benefit_id, enrollment_date });
    });
});

app.delete('/api/employee-benefits/:id', (req, res) => {
  db.run('DELETE FROM employee_benefits WHERE id = ?', [req.params.id], function(err) {
    if (err) return res.status(500).json({ error: err.message });
    res.json({ deleted: this.changes });
  });
});

const PORT = 3001;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
