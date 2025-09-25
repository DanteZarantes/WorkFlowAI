# NeuralFlow - AI-Powered Business Solutions Platform

A Django-based web application that provides AI-powered business solutions with user management, task organization, and JSON-based data storage.

## 🚀 Features

### Core Functionality
- **User Authentication & Profiles** - Custom user system with extended profiles
- **Task Management** - Create, organize, and track tasks with JSON storage
- **Project Organization** - Manage projects with team collaboration features
- **JSON Data Storage** - Automatic data persistence in organized JSON files
- **Activity Tracking** - Comprehensive user activity logging
- **Dashboard Analytics** - Real-time statistics and data visualization

### User Management
- **Registration System** - Secure user registration with email validation
- **Login System** - Email/username authentication with activity logging
- **Profile Management** - Extended user profiles with skills and preferences
- **User Directory** - Connect with other users in the platform

### Data Management
- **JSON Storage System** - Automatic data saving to organized JSON files
- **Task Organization** - Priority-based task management with categories
- **Project Tracking** - Project status, timeline, and team management
- **Backup System** - Automated data backup and recovery

## 🛠️ Technology Stack

### Backend
- **Django 5.1.3** - Python web framework
- **Django REST Framework** - API development
- **SQLite** - Database for user authentication
- **Custom User Model** - Extended authentication system
- **JSON Storage** - File-based data persistence

### Frontend
- **HTML/CSS/JavaScript** - Standard web technologies
- **CSS Grid & Flexbox** - Responsive layouts
- **Django Templates** - Server-side rendering
- **Bootstrap Components** - UI framework

## 📁 Project Structure

```
NeuralFlow1.0/
├── config/               # Django configuration
│   ├── settings/         # Environment-specific settings
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI configuration
├── core/                 # Main application logic
│   ├── management/       # Custom Django commands
│   ├── views.py          # Core views
│   └── models.py         # Core models
├── accounts/             # User management
│   ├── models.py         # User models
│   ├── views.py          # Authentication views
│   ├── forms.py          # User forms
│   └── api_views.py      # API endpoints
├── utils/                # Utility functions
│   ├── json_storage.py   # JSON data management
│   ├── data_initializer.py # Data setup utilities
│   └── middleware.py     # Custom middleware
├── data/                 # JSON data storage
│   ├── users/            # User data files
│   ├── tasks/            # Task data files
│   ├── projects/         # Project data files
│   └── models/           # AI model data files
├── templates/            # HTML templates
├── static/               # Static assets
├── docs/                 # Documentation
└── manage.py             # Django management
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.9+ installed
- Git installed
- Virtual environment tool (venv)

### Setup Steps
```bash
# Clone the repository
git clone <your-repo-url>
cd NeuralFlow1.0

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Initialize JSON data system
python manage.py setup_data --sync-users

# Start development server
python manage.py runserver
```

## 🌐 Usage

### Application URLs
- **Main Application**: `http://localhost:8000`
- **Admin Panel**: `http://localhost:8000/admin`
- **User Registration**: `http://localhost:8000/accounts/signup/`
- **User Login**: `http://localhost:8000/accounts/login/`
- **Dashboard**: `http://localhost:8000/dashboard/`

### Key Features
- **User Registration**: Create new accounts with automatic JSON data storage
- **Task Management**: Create and organize tasks via API endpoints
- **Project Management**: Manage projects with team collaboration
- **Dashboard**: View statistics and recent activities
- **Profile Management**: Update user profiles and preferences

## 🔒 Security Features

- **Django Authentication** - Built-in user authentication system
- **CSRF Protection** - Cross-site request forgery prevention
- **SQL Injection Prevention** - Django ORM protection
- **Session Security** - Secure session management
- **Password Validation** - Strong password requirements
- **Data Isolation** - User-specific JSON file storage
- **Activity Logging** - Comprehensive user activity tracking

## 📊 Data Models

### Database Models
- **CustomUser** - Extended user model with business features
- **UserProfile** - Additional profile information
- **UserActivity** - Activity tracking and analytics
- **AIModel** - AI model configurations and metadata
- **Project** - User project organization
- **UserConnection** - User networking system

### JSON Data Structure
- **User Data** - Complete user profiles in `data/users/`
- **Task Data** - Task management in `data/tasks/`
- **Project Data** - Project information in `data/projects/`
- **Model Data** - AI model configurations in `data/models/`

## 📝 API Endpoints

### Task Management
- `POST /accounts/api/tasks/` - Create new task
- `GET /accounts/api/tasks/` - Get user tasks

### Project Management
- `POST /accounts/api/projects/` - Create new project
- `GET /accounts/api/projects/` - Get user projects

### AI Model Management
- `POST /accounts/api/models/` - Create new AI model
- `GET /accounts/api/models/` - Get user AI models

### Dashboard Data
- `GET /accounts/api/dashboard/` - Get dashboard statistics

## 🔧 Management Commands

```bash
# Initialize data system
python manage.py setup_data

# Sync existing users to JSON
python manage.py setup_data --sync-users

# Validate data integrity
python manage.py setup_data --validate

# Create data backup
python manage.py setup_data --backup

# Show storage statistics
python manage.py setup_data --stats
```

## 🧪 Testing

```bash
# Run comprehensive JSON storage tests
python test_json_storage.py

# Run Django tests
python manage.py test

# Check system configuration
python manage.py check
```

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:
- `SETUP.md` - Detailed setup instructions
- `DATA_SYSTEM.md` - JSON storage system documentation
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Custom Settings
- `config/settings/development.py` - Local development
- `config/settings/production.py` - Production deployment
- `config/settings/base.py` - Shared settings

---

**Built with Django for scalable business task management and user collaboration.**