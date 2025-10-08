# WorkFlowAI - AI-Powered Business Solutions Platform

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
WorkFlowAI/
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
- **Python 3.9+** - Download from [python.org](https://python.org)
- **Git** - Download from [git-scm.com](https://git-scm.com)
- **Node.js 16+** (optional, for frontend development)
- **Virtual environment tool** (venv or virtualenv)

### Quick Setup (5 minutes)
```bash
# 1. Clone the repository
git clone https://github.com/your-username/WorkFlowAI.git
cd NeuralFlow1.3broken

# 2. Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Setup database and create admin user
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 5. Start the development server
python manage.py runserver
```

### 🚀 Access Your Application
After setup, open your browser and navigate to:
- **Main App**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Project Boards**: http://localhost:8000/boards
- **API Documentation**: http://localhost:8000/api/docs

### 🔧 Advanced Setup Options

#### Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your settings
# SECRET_KEY=your-secret-key-here
# DEBUG=True
# ALLOWED_HOSTS=localhost,127.0.0.1
```

#### Frontend Development (Optional)
```bash
# Install Node.js dependencies
cd frontend
npm install

# Start frontend development server
npm run dev

# Build for production
npm run build
```

#### Docker Setup (Alternative)
```bash
# Build and run with Docker
docker-compose up --build

# Access at http://localhost:8000
```

## 🌐 Usage Guide

### 📱 Core Features

#### **Project Boards** - Visual Task Management
- **Kanban Boards**: Drag-and-drop task organization
- **Task Tree**: Hierarchical task breakdown (1, 1.1, 1.1.1, etc.)
- **Mind Maps**: Visual project planning with D3.js
- **Real-time Sync**: Collaborative workspace updates

#### **Task Management** - Smart Organization
- **Hierarchical Numbering**: Auto-generated task numbers (1.1.2, 2.3.1)
- **Subtask Creation**: Unlimited nesting levels
- **Priority System**: Critical, High, Medium, Low priorities
- **Status Tracking**: Todo, In Progress, Review, Done
- **Due Date Management**: Calendar integration with overdue alerts

#### **Advanced Visualizations** - D3.js Powered
- **Interactive Task Trees**: Collapsible hierarchical views
- **Dynamic Mind Maps**: Drag-and-drop node positioning
- **Real-time Updates**: Live collaboration features
- **Multiple Layouts**: Tree, Cluster, and Radial views

### 🎯 Quick Start Workflow

1. **Create Account** → Register at `/accounts/signup/`
2. **Create Board** → Go to Project Boards
3. **Add Tasks** → Use Task Tree or Mind Map
4. **Organize** → Drag, drop, and nest tasks
5. **Collaborate** → Share boards with team members
6. **Track Progress** → Monitor via Dashboard analytics

### 🔗 Application URLs
- **🏠 Home**: `http://localhost:8000`
- **📊 Dashboard**: `http://localhost:8000/dashboard/`
- **📋 Project Boards**: `http://localhost:8000/boards/`
- **🌳 Task Tree**: `http://localhost:8000/task-tree/`
- **🧠 Mind Map**: `http://localhost:8000/mindmap/`
- **⚙️ Admin Panel**: `http://localhost:8000/admin/`
- **📚 API Docs**: `http://localhost:8000/api/docs/`

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

### Data Management
```bash
# Initialize complete data system
python manage.py setup_data

# Sync existing users to JSON storage
python manage.py setup_data --sync-users

# Validate all data integrity
python manage.py setup_data --validate

# Create comprehensive backup
python manage.py setup_data --backup

# Display storage statistics
python manage.py setup_data --stats

# Clean orphaned data
python manage.py setup_data --cleanup
```

### Board Management
```bash
# Initialize board system
python manage.py init_boards

# Fix board isolation issues
python manage.py fix_board_isolation

# Sync enhanced models
python manage.py sync_enhanced_models

# Fix user data consistency
python manage.py fix_user_data
```

### Development Utilities
```bash
# Create sample data for testing
python manage.py create_sample_data

# Reset database (development only)
python manage.py flush

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser
```

## 🧪 Testing & Quality Assurance

### Unit Tests
```bash
# Run all tests
python manage.py test

# Run specific test modules
python manage.py test accounts
python manage.py test core

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Storage System Tests
```bash
# Test JSON storage system
python test_json_storage.py

# Test board isolation
python test_board_isolation.py

# Validate data integrity
python manage.py setup_data --validate
```

### System Health Checks
```bash
# Django system check
python manage.py check

# Check deployment readiness
python manage.py check --deploy

# Database consistency
python manage.py dbshell
```

### Performance Testing
```bash
# Load testing with locust
pip install locust
locust -f tests/load_test.py

# Memory profiling
pip install memory-profiler
python -m memory_profiler manage.py runserver
```

## 📚 Documentation

Detailed documentation is available in the `docs/` folder:
- `SETUP.md` - Detailed setup instructions
- `DATA_SYSTEM.md` - JSON storage system documentation
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details

## ⚙️ Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:
```env
# Security
SECRET_KEY=your-super-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database (Optional - defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/workflowai

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Storage
STATIC_ROOT=/var/www/workflowai/static/
MEDIA_ROOT=/var/www/workflowai/media/

# Security Headers
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### Settings Structure
```
config/settings/
├── base.py          # Shared settings
├── development.py   # Local development
├── production.py    # Production deployment
└── testing.py       # Test environment
```

### Custom Configuration
```python
# config/settings/local.py (create for personal settings)
from .development import *

# Override any settings
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Custom database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'workflowai_dev',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

**Built with Django for scalable business task management and user collaboration.**