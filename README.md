# NeuralFlow - AI-Powered Business Solutions Platform

A comprehensive full-stack web application that provides AI-powered business solutions with a modern React/Next.js frontend and robust Django REST API backend.

## 🚀 Features

### Core Functionality
- **User Authentication & Profiles** - Custom user system with extended profiles
- **AI Model Management** - Create, train, and deploy AI models
- **Project Organization** - Organize AI models into projects
- **API Usage Tracking** - Monitor and limit API calls with detailed analytics
- **User Connections** - Connect with other AI professionals and researchers
- **Real-time Notifications** - Stay updated with system and user activities

### AI Tools & Services
- **Cost Calculator** - Interactive tool to estimate AI service costs
- **Text Analyzer** - Sentiment analysis, readability scoring, and keyword extraction
- **Color Palette Generator** - AI-powered color scheme generation
- **Chatbot Builder** - Create intelligent conversational agents
- **Computer Vision** - Image and video analysis capabilities
- **Machine Learning Platform** - Custom ML model development

### Modern UI/UX
- **Responsive Design** - Mobile-first approach with CSS Grid layouts
- **Interactive Components** - React-powered dynamic interfaces
- **Theme Customization** - Multiple color themes and display preferences
- **Floating Animations** - Smooth background animations and effects
- **Professional Navigation** - Hamburger menu with organized sidebar

## 🛠️ Technology Stack

### Backend
- **Django 5.1.3** - Python web framework
- **Django REST Framework** - API development
- **SQLite/PostgreSQL** - Database options
- **Custom User Model** - Extended authentication system
- **CORS Headers** - Cross-origin request handling

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **CSS Grid & Flexbox** - Advanced responsive layouts
- **React Hooks** - Modern state management
- **Chart.js** - Data visualization
- **Three.js** - 3D graphics and animations

## 📁 Project Structure

```
neuralflow/
├── backend/               # Django REST API
│   ├── config/           # Django configuration
│   ├── core/             # Main application logic
│   ├── accounts/         # User management
│   ├── utils/            # Utility functions
│   ├── templates/        # HTML templates
│   ├── static/           # Static assets
│   ├── media/            # User uploads
│   ├── logs/             # Application logs
│   └── manage.py         # Django management
├── frontend/             # Next.js application
│   ├── app/              # App router pages
│   ├── components/       # React components
│   └── styles/           # CSS modules
├── docs/                 # Documentation
└── README.md             # This file
```

## 🔧 Installation & Setup

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Environment setup
cp .env.example .env
# Edit .env with your configuration

# Database setup
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## 🌐 Usage

### Development URLs
- **Django Backend**: `http://localhost:8000`
- **Next.js Frontend**: `http://localhost:3000`
- **Admin Panel**: `http://localhost:8000/admin`
- **API Documentation**: `http://localhost:8000/api/docs`

### Key Features Access
- **AI Tools**: Available in the main navigation and sidebar
- **User Directory**: Connect with other users via profile dropdown
- **Theme Settings**: Customize appearance through user menu
- **Dashboard**: Monitor your AI models and usage statistics

## 🔒 Security Features

- **Environment Variables** - Sensitive data protection
- **CSRF Protection** - Cross-site request forgery prevention
- **SQL Injection Prevention** - Django ORM protection
- **File Upload Validation** - Secure file handling
- **Rate Limiting** - API usage controls
- **Session Security** - Secure session management
- **Password Validation** - Strong password requirements

## 📊 Database Models

### Core Models
- **AIModel** - AI model configurations and metadata
- **Project** - User project organization
- **APIUsage** - API call tracking and analytics
- **UserConnection** - User networking system
- **Notification** - Real-time user notifications
- **FileUpload** - Secure file management

### User Models
- **CustomUser** - Extended user with business features
- **UserProfile** - Additional profile information
- **UserActivity** - Activity tracking and analytics

## 🚀 Deployment

### Environment Configuration
1. Set production environment variables
2. Configure database (PostgreSQL recommended)
3. Set up static file serving
4. Configure email backend
5. Enable security settings

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Configure secure `SECRET_KEY`
- [ ] Set up HTTPS
- [ ] Configure database backups
- [ ] Set up monitoring and logging
- [ ] Configure email service
- [ ] Set up CDN for static files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 API Documentation

The API provides endpoints for:
- User authentication and management
- AI model CRUD operations
- Project management
- Usage analytics
- File uploads
- User connections

Access the interactive API documentation at `/api/docs` when running the development server.

## 🔧 Configuration

### Environment Variables
See `backend/.env.example` for all available configuration options including:
- Database settings
- Email configuration
- API keys
- Security settings
- Feature flags

### Custom Settings
The application supports multiple environment configurations:
- `development.py` - Local development
- `production.py` - Production deployment
- `base.py` - Shared settings

---

**Built with modern web technologies for scalable AI-powered business solutions.**