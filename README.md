# HR Management & Payroll Suite
ICT712 Group 5 — Enterprise Systems Development, Semester 1 2026

## First-time setup (every member runs this once after cloning)

1. Clone the repo:
   git clone https://github.com/YOUR_USERNAME/hr-payroll-suite.git
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

Terminal 1 — Django server:
   python manage.py runserver

Terminal 2 — Celery worker:
   celery -A config worker --loglevel=info

Terminal 3 — Redis:
   sudo service redis-server start

## Branch rules — READ THIS
- NEVER push directly to main or dev
- Always work on your own feature branch (see table above)
- When your task is done, open a Pull Request to dev
- Tag Ashish as reviewer on every PR
- Pull from dev before starting any new work



<!-- ERROR IN STEP 11 -->