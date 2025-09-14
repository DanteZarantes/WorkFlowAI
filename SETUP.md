# NeuralFlow Setup Guide

## Quick Start

### 1. Prerequisites
- Python 3.9+ installed
- Git installed
- Virtual environment tool (venv)

### 2. Installation Steps

```bash
# Clone the repository
git clone <your-repo-url>
cd neuralflow

# Create and activate virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
copy .env.example .env
# Edit .env file with your settings

# Set up database
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Start development server
python manage.py runserver
```

### 3. Access the Application

- **Main Site**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **API Docs**: http://localhost:8000/api/docs

### 4. Key Commands

```bash
# Start server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

### 5. Project Structure

```
neuralflow/
├── manage.py              # Django management commands
├── config/                # Django configuration
│   ├── settings/         # Environment-specific settings
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI configuration
├── core/                 # Main application
├── accounts/             # User authentication
├── utils/                # Utility functions
├── templates/            # HTML templates
├── static/               # Static files (CSS, JS)
├── media/                # User uploads
└── requirements.txt      # Python dependencies
```

### 6. Environment Variables

Copy `.env.example` to `.env` and configure:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 7. Troubleshooting

**Common Issues:**

1. **Import Errors**: Make sure virtual environment is activated
2. **Database Errors**: Run `python manage.py migrate`
3. **Static Files**: Run `python manage.py collectstatic`
4. **Permission Errors**: Check file permissions

**Getting Help:**
- Check the logs in `logs/django.log`
- Use `python manage.py check` to validate configuration
- Run `python manage.py test` to verify everything works