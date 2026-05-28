# HR Management & Payroll Suite
ICT712 Group 5 — Enterprise Systems Development, Semester 1 2026

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
   git clone https://github.com/Asheesh7/hr-payroll-suite.git
   cd hr-payroll-suite

2. Create virtual environment:
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Set up environment:
   cp .env.example .env
   (open .env and set your own DB_PASSWORD)

5. Set up database:
   python manage.py migrate
   python manage.py createsuperuser

## Running the project (open 3 terminals, venv active in all)

Terminal 1 -Celery worker:
   celery -A config worker --loglevel=info

Terminal 2 - Redis:
   sudo service redis-server start

Terminal 3 - Django Server
   python manage.py runserver

Then open: `http://127.0.0.1:8000/employees/login/`


## Authors

**ICT712 Enterprise Systems Development — Group 5 (Melbourne Campus)**

- Ashish Prasai (61722) — Team Leader
- Susmita Giri (63232)
- Angelin Akshitha Martin Rajendra Mohan (66465)
- Pubudu Navamalika Pallage Dona (64803)
- Vinuri Ushana Weerasinghe Arachchige (64816)

---

## License

This project is developed for academic purposes as part of the ICT712 coursework.
