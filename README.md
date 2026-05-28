# HR Management & Payroll Suite
ICT712 Group 5 - Enterprise Systems Development, Semester 1 2026

An enterprise web application for managing HR records, leave requests, payroll processing, and performance reviews — built with Django 5.0, MySQL, Redis, and Celery.

## Features
- **Employee Management** — employee records, departments, and user authentication
- **Leave Management** — request submission, manager approvals, atomic leave balance deduction
- **Payroll Processing** — salary structures, configurable tax brackets, payslip generation, email distribution
- **Performance Reviews** — manager-driven ratings and feedback with reporting
- **Role-Based Access Control (RBAC)** — four organisational roles (Employee, Line Manager, HR Officer, Payroll Administrator)
- **Asynchronous Background Tasks** — email notifications powered by Celery and Redis
- **Atomic Transactions** — data integrity guaranteed during concurrent operations
- **System-Wide Audit Trail** — all user actions logged with timestamps

---

## Tech Stack

Python 3.12 · Django 5.0 · MySQL 8.0 · Redis 7.0 · Celery 5.3 · ReportLab 4.1

---

## First-time setup 

1. Clone the repo:
   ```bash
   git clone https://github.com/Asheesh7/hr-payroll-suite.git
   cd hr-payroll-suite
   ```
### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create the MySQL database

```sql
CREATE DATABASE hrpayroll_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Set up environment variables

Create a `.env` file in the project root with:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=hrpayroll_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
REDIS_URL=redis://localhost:6379/0
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Replace `your_mysql_password` with your actual MySQL password.

### 6. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create superuser and role groups

```bash
python manage.py createsuperuser
python manage.py create_groups
```

---

## Running the Project

Open three terminals (virtual environment active in all).

### Terminal 1 - Redis Server

**Windows:**

```bash
redis-server
```

**Linux:**

```bash
sudo service redis-server start
```

### Terminal 2 - Celery Worker

```bash
celery -A config worker --loglevel=info
```

### Terminal 3 - Django Server

```bash
python manage.py runserver
```

Then open: `http://127.0.0.1:8000/employees/login/`

---
## Authors

**ICT712 Enterprise Systems Development - Group 5 (Melbourne Campus)**

- Ashish Prasai (61722) — Team Leader
- Susmita Giri (63232)
- Angelin Akshitha Martin Rajendra Mohan (66465)
- Pubudu Navamalika Pallage Dona (64803)
- Vinuri Ushana Weerasinghe Arachchige (64816)

---

## License

This project is developed for academic purposes as part of the ICT712 coursework.
