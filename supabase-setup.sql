-- Run this SQL in Supabase SQL Editor
-- Go to: Supabase Dashboard → SQL Editor → New Query

-- Create benefits table
CREATE TABLE IF NOT EXISTS benefits (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  cost REAL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT,
  department TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create employee_benefits junction table
CREATE TABLE IF NOT EXISTS employee_benefits (
  id BIGSERIAL PRIMARY KEY,
  employee_id BIGINT REFERENCES employees(id) ON DELETE CASCADE,
  benefit_id BIGINT REFERENCES benefits(id) ON DELETE CASCADE,
  enrollment_date TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Disable Row Level Security (RLS) for testing
-- WARNING: In production, you should enable RLS and create proper policies
ALTER TABLE benefits DISABLE ROW LEVEL SECURITY;
ALTER TABLE employees DISABLE ROW LEVEL SECURITY;
ALTER TABLE employee_benefits DISABLE ROW LEVEL SECURITY;

-- Optional: Insert some sample data
INSERT INTO benefits (name, description, cost) VALUES
  ('Health Insurance', 'Comprehensive health coverage', 500.00),
  ('Dental Insurance', 'Dental and vision coverage', 150.00),
  ('401k Match', 'Company 401k matching up to 6%', 0.00);

INSERT INTO employees (name, email, department) VALUES
  ('John Doe', 'john@example.com', 'Engineering'),
  ('Jane Smith', 'jane@example.com', 'HR'),
  ('Bob Johnson', 'bob@example.com', 'Sales');
