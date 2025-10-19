import express from 'express';
import { createClient } from '@supabase/supabase-js';
import cors from 'cors';

const app = express();

// Initialize Supabase client
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
);

app.use(cors());
app.use(express.json());

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
      .select(`
        id,
        employee_id,
        benefit_id,
        enrollment_date,
        benefits (name),
        employees (name)
      `);
    
    if (error) throw error;
    
    const formattedData = (data || []).map(eb => ({
      id: eb.id,
      employee_id: eb.employee_id,
      benefit_id: eb.benefit_id,
      enrollment_date: new Date(eb.enrollment_date).toLocaleDateString(),
      benefit_name: eb.benefits?.name || 'Unknown',
      employee_name: eb.employees?.name || 'Unknown'
    }));
    
    res.json(formattedData);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/api/employee-benefits', async (req, res) => {
  const { employee_id, benefit_id } = req.body;
  try {
    const { data, error } = await supabase
      .from('employee_benefits')
      .insert([{ employee_id, benefit_id }])
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

export default app;
