# HR Benefits Management System

A full-stack application for HR managers to manage employee benefits.

## Features

- **Manage Benefits**: Add, view, and delete benefits
- **Manage Employees**: Add and view employees
- **Employee Benefits**: Enroll employees in benefits and view current enrollments

## Database

SQLite database with 3 tables:
- `benefits`: Stores benefit information
- `employees`: Stores employee information
- `employee_benefits`: Links employees to their enrolled benefits

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the backend server:
```bash
npm run server
```

3. In a new terminal, start the frontend:
```bash
npm run dev
```

4. Open http://localhost:5173 in your browser

## API Endpoints

- GET/POST `/api/benefits` - Manage benefits
- DELETE `/api/benefits/:id` - Delete benefit
- GET/POST `/api/employees` - Manage employees
- GET/POST `/api/employee-benefits` - Manage enrollments
- DELETE `/api/employee-benefits/:id` - Remove enrollment
