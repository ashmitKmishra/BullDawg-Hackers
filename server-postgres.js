import express from 'express';
import pkg from 'pg';
const { Pool } = pkg;
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();

// PostgreSQL connection pool
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false
  }
});

app.use(cors());
app.use(express.json());

// Initialize database tables
const initDatabase = async () => {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS benefits (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        cost REAL
      )
    `);

    await pool.query(`
      CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT,
        department TEXT
      )
    `);

    await pool.query(`
      CREATE TABLE IF NOT EXISTS employee_benefits (
        id SERIAL PRIMARY KEY,
        employee_id INTEGER REFERENCES employees(id),
        benefit_id INTEGER REFERENCES benefits(id),
        enrollment_date TEXT
      )
    `);

    console.log('Database tables initialized successfully');
  } catch (err) {
    console.error('Error initializing database:', err);
  }
};

initDatabase();


// Benefits endpoints
app.get('/api/benefits', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM benefits');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/benefits', async (req, res) => {
  const { name, description, cost } = req.body;
  try {
    const result = await pool.query(
      'INSERT INTO benefits (name, description, cost) VALUES ($1, $2, $3) RETURNING *',
      [name, description, cost]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.delete('/api/benefits/:id', async (req, res) => {
  try {
    const result = await pool.query('DELETE FROM benefits WHERE id = $1', [req.params.id]);
    res.json({ deleted: result.rowCount });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});


// Employees endpoints
app.get('/api/employees', async (req, res) => {
  try {
    const result = await pool.query('SELECT * FROM employees');
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/employees', async (req, res) => {
  const { name, email, department } = req.body;
  try {
    const result = await pool.query(
      'INSERT INTO employees (name, email, department) VALUES ($1, $2, $3) RETURNING *',
      [name, email, department]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});


// Employee benefits endpoints
app.get('/api/employee-benefits', async (req, res) => {
  const query = `
    SELECT eb.id, e.name as employee_name, e.email, b.name as benefit_name, 
           eb.enrollment_date, e.id as employee_id, b.id as benefit_id
    FROM employee_benefits eb
    JOIN employees e ON eb.employee_id = e.id
    JOIN benefits b ON eb.benefit_id = b.id
  `;
  try {
    const result = await pool.query(query);
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/employee-benefits', async (req, res) => {
  const { employee_id, benefit_id } = req.body;
  const enrollment_date = new Date().toISOString().split('T')[0];
  try {
    const result = await pool.query(
      'INSERT INTO employee_benefits (employee_id, benefit_id, enrollment_date) VALUES ($1, $2, $3) RETURNING *',
      [employee_id, benefit_id, enrollment_date]
    );
    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.delete('/api/employee-benefits/:id', async (req, res) => {
  try {
    const result = await pool.query('DELETE FROM employee_benefits WHERE id = $1', [req.params.id]);
    res.json({ deleted: result.rowCount });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
