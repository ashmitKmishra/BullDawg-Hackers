import express from 'express';
import { createClient } from '@supabase/supabase-js';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();

// Initialize Supabase client
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
);

app.use(cors());
app.use(express.json());

// Test connection
supabase.from('benefits').select('count').limit(1).then(({ error }) => {
  if (error) {
    console.log('⚠️  Please create tables in Supabase Table Editor');
  } else {
    console.log('✅ Connected to Supabase database!');
  }
});

// Benefits endpoints
app.get('/api/benefits', async (req, res) => {
  try {
    const { data, error } = await supabase.from('benefits').select('*');
    if (error) throw error;
    res.json(data || []);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/benefits', async (req, res) => {
  const { name, description, cost } = req.body;
  try {
    const { data, error } = await supabase
      .from('benefits')
      .insert([{ name, description, cost }])
      .select()
      .single();
    if (error) throw error;
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.delete('/api/benefits/:id', async (req, res) => {
  try {
    const { error } = await supabase.from('benefits').delete().eq('id', req.params.id);
    if (error) throw error;
    res.json({ deleted: 1 });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Employees endpoints
app.get('/api/employees', async (req, res) => {
  try {
    const { data, error } = await supabase.from('employees').select('*');
    if (error) throw error;
    res.json(data || []);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/employees', async (req, res) => {
  const { name, email, department } = req.body;
  try {
    const { data, error } = await supabase
      .from('employees')
      .insert([{ name, email, department }])
      .select()
      .single();
    if (error) throw error;
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Employee benefits endpoints
app.get('/api/employee-benefits', async (req, res) => {
  try {
    const { data, error } = await supabase
      .from('employee_benefits')
      .select('id, enrollment_date, employee_id, benefit_id, employees(id, name, email), benefits(id, name)');
    if (error) throw error;
    const formatted = (data || []).map(item => ({
      id: item.id,
      employee_id: item.employee_id,
      benefit_id: item.benefit_id,
      employee_name: item.employees?.name,
      email: item.employees?.email,
      benefit_name: item.benefits?.name,
      enrollment_date: item.enrollment_date
    }));
    res.json(formatted);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/employee-benefits', async (req, res) => {
  const { employee_id, benefit_id } = req.body;
  const enrollment_date = new Date().toISOString().split('T')[0];
  try {
    const { data, error } = await supabase
      .from('employee_benefits')
      .insert([{ employee_id, benefit_id, enrollment_date }])
      .select()
      .single();
    if (error) throw error;
    res.json(data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.delete('/api/employee-benefits/:id', async (req, res) => {
  try {
    const { error } = await supabase.from('employee_benefits').delete().eq('id', req.params.id);
    if (error) throw error;
    res.json({ deleted: 1 });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
