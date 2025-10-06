# WorkFlowAI - Complete Setup Guide

## 🚀 Quick Start (5 Minutes)

### Prerequisites Check
```bash
# Check Python version (3.9+ required)
python --version

# Check Git installation
git --version

# Check Node.js (optional, for frontend)
node --version
```

### 1. Clone and Setup
```bash
# Clone repository
git clone https://github.com/your-username/WorkFlowAI.git
cd WorkFlowAI

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Follow prompts to create username, email, password
```

### 3. Initialize Data System
```bash
# Setup JSON storage system
python manage.py setup_data --sync-users

# Initialize board system
python manage.py init_boards

# Create sample data (optional)
python manage.py create_sample_data
```

### 4. Start Development Server
```bash
python manage.py runserver
```

**🎉 Success!** Open http://localhost:8000 in your browser.

---

## 🔧 Detailed Configuration

### Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env file
nano .env  # or use your preferred editor
```

**Required .env variables:**
```env
SECRET_KEY=your-secret-key-here-make-it-long-and-random
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration

#### SQLite (Default - No setup needed)
```python
# Already configured in settings/development.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### PostgreSQL (Production Recommended)
```bash
# Install PostgreSQL
# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# macOS:
brew install postgresql

# Windows: Download from postgresql.org
```

```env
# Add to .env
DATABASE_URL=postgresql://username:password@localhost:5432/workflowai
```

#### MySQL (Alternative)
```bash
# Install MySQL
# Ubuntu/Debian:
sudo apt-get install mysql-server

# macOS:
brew install mysql
```

```env
# Add to .env
DATABASE_URL=mysql://username:password@localhost:3306/workflowai
```

---

## 🎯 Feature Configuration

### Task Tree & Mind Map Setup
The application uses D3.js for advanced visualizations:

```javascript
// Task Tree Features:
- Hierarchical numbering (1, 1.1, 1.1.1, 1.1.2, 1.2, 2, etc.)
- Collapsible nodes
- Drag-and-drop positioning
- Multiple layout options (Tree, Cluster, Radial)
- Real-time collaboration

// Mind Map Features:
- Visual node connections
- Drag-and-drop positioning
- Hierarchical numbering
- Status-based coloring
- Interactive editing
```

### Board System Configuration
```bash
# Initialize board isolation
python manage.py fix_board_isolation

# Sync enhanced models
python manage.py sync_enhanced_models
```

---

## 🚀 Production Deployment

### 1. Server Requirements
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Amazon Linux 2
- **Python**: 3.9+
- **Memory**: 2GB+ RAM
- **Storage**: 10GB+ SSD
- **Database**: PostgreSQL 12+ (recommended)

### 2. Production Setup
```bash
# Clone on server
git clone https://github.com/your-username/WorkFlowAI.git
cd WorkFlowAI

# Create production environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Production settings
export DJANGO_SETTINGS_MODULE=config.settings.production
```

### 3. Environment Configuration
```env
# Production .env
SECRET_KEY=your-super-secure-production-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/workflowai_prod

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Email
EMAIL_HOST=smtp.your-provider.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@your-domain.com
EMAIL_HOST_PASSWORD=your-email-password
```

### 4. Web Server Setup (Nginx + Gunicorn)
```bash
# Install Nginx
sudo apt-get install nginx

# Install Gunicorn
pip install gunicorn

# Create Gunicorn service
sudo nano /etc/systemd/system/workflowai.service
```

**Gunicorn service file:**
```ini
[Unit]
Description=WorkFlowAI Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/WorkFlowAI
Environment="PATH=/var/www/WorkFlowAI/venv/bin"
ExecStart=/var/www/WorkFlowAI/venv/bin/gunicorn --workers 3 --bind unix:/var/www/WorkFlowAI/workflowai.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/WorkFlowAI;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/WorkFlowAI/workflowai.sock;
    }
}
```

### 5. SSL Setup (Let's Encrypt)
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python manage.py runserver 8001
```

#### 2. Database Connection Error
```bash
# Check database service
sudo systemctl status postgresql

# Restart database
sudo systemctl restart postgresql

# Check connection
python manage.py dbshell
```

#### 3. Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic

# Check static files settings
python manage.py check --deploy
```

#### 4. Permission Errors
```bash
# Fix file permissions
chmod -R 755 /path/to/WorkFlowAI
chown -R www-data:www-data /path/to/WorkFlowAI
```

### Debug Mode
```bash
# Enable debug logging
export DJANGO_LOG_LEVEL=DEBUG

# Run with verbose output
python manage.py runserver --verbosity=2
```

### Performance Issues
```bash
# Check system resources
htop

# Monitor database queries
python manage.py shell
>>> from django.db import connection
>>> print(len(connection.queries))

# Profile memory usage
pip install memory-profiler
python -m memory_profiler manage.py runserver
```

---

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# System health
python manage.py check --deploy

# Database integrity
python manage.py setup_data --validate

# Storage statistics
python manage.py setup_data --stats
```

### Backup Strategy
```bash
# Database backup
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# JSON storage backup
python manage.py setup_data --backup

# Full system backup
tar -czf workflowai_backup_$(date +%Y%m%d).tar.gz /var/www/WorkFlowAI
```

### Log Management
```bash
# View Django logs
tail -f logs/django.log

# View system logs
sudo journalctl -u workflowai -f

# Rotate logs
sudo logrotate /etc/logrotate.d/workflowai
```

---

## 🆘 Support

### Getting Help
- **Documentation**: Check `/docs` folder
- **Issues**: Create GitHub issue with logs
- **Community**: Join our Discord/Slack
- **Email**: support@workflowai.com

### Reporting Bugs
Include:
1. Python version: `python --version`
2. Django version: `python -m django --version`
3. OS information: `uname -a`
4. Error logs from `logs/django.log`
5. Steps to reproduce

### Feature Requests
- Use GitHub Issues with `enhancement` label
- Provide detailed use case
- Include mockups if applicable

---

**🎉 Congratulations!** You now have WorkFlowAI running successfully.

For advanced configuration and customization, check the `/docs` folder for detailed guides.