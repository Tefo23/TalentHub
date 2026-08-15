TalentHub
TalentHub is a Django-based talent and recruitment web application that connects job seekers and employers. The application provides authentication, candidate and employer dashboards, job posting and discovery, applications, profiles, messaging, and contact functionality.

Live Application
Hosted URL: https://talenthub-as9a.onrender.com

The application is deployed on Render with PostgreSQL as the production database.

Main Features
User registration and login

Separate job-seeker and employer roles

Candidate dashboard

Employer dashboard

Candidate profile management

Employer/company profile management

Job creation and job browsing

Job search and filtering by keyword, location, and employment type

Job applications and application tracking

Application withdrawal for eligible statuses

Messaging functionality

Contact form

Profile pictures and company logos

Django administration interface

Responsive static assets served in production with WhiteNoise

Technology Stack
Backend: Python, Django

Database: PostgreSQL

Database driver: psycopg2-binary

Production server: Gunicorn

Static files: WhiteNoise + Django collectstatic

Deployment: Render

Version control: Git and GitHub

Image handling: Pillow

Project Structure
TalentHub/
├── accounts/                 # Authentication, registration, dashboards, public pages
├── applications/             # Application-related functionality
├── contacts/                 # Contact functionality
├── jobs/                     # Job-related functionality
├── messaging/                # Messaging functionality
├── profiles/                 # Candidate and employer profiles
├── static/                   # Source static assets
├── templates/                # Django HTML templates
├── talenthub/                # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── build.sh                 # Render build/deployment commands
├── manage.py                # Django management entry point
├── render.yaml              # Render deployment configuration
├── requirements.txt         # Python dependencies
└── .gitignore               # Files excluded from Git
Local Development Setup
1. Clone or copy the project
Open a terminal in the project directory:

cd C:\Users\<YOUR-USERNAME>\Desktop\TalentHub
2. Create a virtual environment
Windows PowerShell:

py -m venv venv
Activate it:

.\venv\Scripts\Activate.ps1
If PowerShell blocks script execution for the current session, use:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
and activate the environment again.

3. Install dependencies
python -m pip install -r requirements.txt
4. Configure the local PostgreSQL database
Create a PostgreSQL database named talenthub and make sure the PostgreSQL server is running.

The Django project uses the DATABASE_URL environment variable. For a local PowerShell session, an example is:

$env:DATABASE_URL="postgresql://postgres:<YOUR-LOCAL-PASSWORD>@localhost:5432/talenthub"
Do not commit real passwords or other secrets to GitHub.

5. Run migrations
python manage.py migrate
6. Collect static files
python manage.py collectstatic --no-input
7. Start the development server
python manage.py runserver
Open:

http://127.0.0.1:8000/
Production Deployment on Render
The project includes a build.sh file and render.yaml deployment configuration.

Render Web Service
Use the GitHub repository and configure the service with:

Runtime: Python 3
Branch: main
Root Directory: leave blank
Build Command:

./build.sh
Start Command:

gunicorn talenthub.wsgi:application
Required Environment Variables
Configure these in the Render Web Service settings:

DEBUG=False
SECRET_KEY=<production-secret-key>
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<Render PostgreSQL connection string>
The production SECRET_KEY should be generated securely and stored in Render environment variables rather than committed to source control.

Build Process
build.sh performs the following steps:

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
This installs dependencies, prepares static assets, and applies database migrations during deployment.

Security and Configuration
DEBUG is enabled for local development and disabled in production.

Production security settings are activated when DEBUG=False.

The production secret key is supplied through an environment variable.

Database credentials are supplied through DATABASE_URL rather than committed to the repository.

.gitignore excludes the local virtual environment, environment files, Python cache files, generated static files, and other development-only files.

Production traffic is configured to use HTTPS.

Static and Media Files
Static assets are collected into staticfiles/ during deployment and served with WhiteNoise.

User-uploaded media is stored using Django's MEDIA_ROOT configuration. On hosting platforms with ephemeral filesystems, uploaded media may not persist across redeployments or service restarts. For a production system requiring permanent user uploads, object storage or a persistent disk should be configured.

Verification and Testing
The project was verified locally using:

python manage.py check
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py runserver
The production deployment was verified by accessing:

https://talenthub-as9a.onrender.com

The live application should be checked after every production deployment for:

Home page loading

Registration and login

Candidate and employer dashboards

Job browsing/search/filtering

Applications

Profiles

Messaging

Contact form

Static assets and page styling

Image upload functionality

Additional Design / Enhancement Notes
TalentHub includes a role-based experience for job seekers and employers, separate dashboards, searchable job listings, application management, and profile/company management. These features provide a complete recruitment workflow rather than a simple static job board.

For further enhancement, suitable future improvements include saved jobs, richer employer analytics, notifications, advanced candidate filtering, and persistent cloud media storage.

Deployment Considerations
The Render free web service may sleep after periods of inactivity, which can make the first request slower after idle time.

A production deployment should use a strong secret key and secure environment variables.

Persistent storage should be considered for uploaded media in a long-term production environment.

Database backups should be configured for a production application that contains important user or recruitment data.

Submission Contents
The final submission ZIP should include the Django source code and deployment files, including:

accounts/
applications/
contacts/
jobs/
messaging/
profiles/
static/
templates/
talenthub/
build.sh
manage.py
render.yaml
requirements.txt
.gitignore
README.md
The final ZIP should not include:

venv/
.git/
.env
staticfiles/
__pycache__/
*.pyc
Author / Project
Project: TalentHub
Framework: Django
Deployment: Render
Database: PostgreSQL
