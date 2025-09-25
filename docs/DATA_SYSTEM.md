# NeuralFlow JSON Data Storage System

## Overview

NeuralFlow now includes a professional JSON-based data storage system that automatically saves user registration data, tasks, projects, and AI models to separate JSON files. This system provides data persistence, backup capabilities, and easy data management.

## Features

### ✅ Implemented Features

1. **User Data Management**
   - Automatic JSON storage on user registration
   - Profile data synchronization
   - Activity logging and tracking

2. **Task Management**
   - Create, store, and retrieve tasks via API
   - JSON-based task persistence
   - Task categorization and status tracking

3. **Project Management**
   - Project creation and management
   - Team member and technology tracking
   - Project status and priority management

4. **AI Model Management**
   - AI model configuration storage
   - Performance metrics tracking
   - Model status and metadata management

5. **Professional Backend**
   - Django middleware integration
   - Automatic data synchronization
   - Error handling and validation
   - Backup and recovery system

## Directory Structure

```
data/
├── users/           # User registration and profile data
│   ├── user_1.json
│   ├── user_2.json
│   └── _index.json
├── tasks/           # User tasks and to-do items
│   ├── tasks_1.json
│   ├── tasks_2.json
│   └── _index.json
├── projects/        # User projects and collaborations
│   ├── projects_1.json
│   ├── projects_2.json
│   └── _index.json
├── models/          # AI models and configurations
│   ├── models_1.json
│   ├── models_2.json
│   └── _index.json
└── backups/         # Automated backups
    └── 20240101_120000/
```

## Setup Instructions

### 1. Initialize the Data System

```bash
# Run the setup command
python manage.py setup_data

# Sync existing users to JSON storage
python manage.py setup_data --sync-users

# Validate data integrity
python manage.py setup_data --validate

# Create backup
python manage.py setup_data --backup

# Show storage statistics
python manage.py setup_data --stats
```

### 2. Test the System

```bash
# Run the test script
python test_json_storage.py
```

### 3. Start the Server

```bash
python manage.py runserver
```

## API Endpoints

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

## Usage Examples

### Creating a Task

```javascript
fetch('/accounts/api/tasks/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        title: 'Complete AI Model Training',
        description: 'Train the classification model with new dataset',
        priority: 'high',
        status: 'pending',
        category: 'machine_learning',
        due_date: '2024-01-15',
        tags: ['ai', 'training', 'urgent']
    })
});
```

### Creating a Project

```javascript
fetch('/accounts/api/projects/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        name: 'Customer Sentiment Analysis',
        description: 'Analyze customer feedback using NLP',
        status: 'active',
        priority: 'high',
        start_date: '2024-01-01',
        end_date: '2024-03-01',
        team_members: ['john@example.com', 'jane@example.com'],
        technologies: ['Python', 'TensorFlow', 'NLTK'],
        budget: 50000
    })
});
```

### Creating an AI Model

```javascript
fetch('/accounts/api/models/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
        name: 'Sentiment Classifier v2.0',
        description: 'Advanced sentiment analysis model',
        model_type: 'nlp',
        status: 'training',
        accuracy: 0.95,
        training_data_size: 100000,
        parameters: {
            'learning_rate': 0.001,
            'batch_size': 32,
            'epochs': 100
        },
        hyperparameters: {
            'dropout': 0.2,
            'hidden_units': 128
        },
        is_public: false
    })
});
```

## Data Structure Examples

### User Data (user_1.json)
```json
{
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "individual",
  "skill_level": "intermediate",
  "subscription_plan": "free",
  "api_calls_limit": 1000,
  "api_calls_used": 45,
  "date_joined": "2024-01-01T10:00:00",
  "updated_at": "2024-01-01T15:30:00",
  "profile": {
    "skills": ["Python", "Machine Learning", "Data Science"],
    "interests": ["AI", "Deep Learning", "NLP"],
    "experience_years": 3
  },
  "activities": [
    {
      "type": "login",
      "description": "User logged in",
      "timestamp": "2024-01-01T15:30:00"
    }
  ]
}
```

### Task Data (tasks_1.json)
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Complete AI Model Training",
      "description": "Train the classification model",
      "priority": "high",
      "status": "pending",
      "category": "machine_learning",
      "due_date": "2024-01-15",
      "tags": ["ai", "training"],
      "created_at": "2024-01-01T10:00:00",
      "user_id": 1
    }
  ],
  "updated_at": "2024-01-01T10:00:00"
}
```

## Security Features

- **Data Validation**: All JSON data is validated before storage
- **Error Handling**: Robust error handling prevents data corruption
- **Backup System**: Automatic backup creation and management
- **Access Control**: User-specific data isolation
- **Activity Logging**: Comprehensive activity tracking

## Monitoring and Maintenance

### Check Storage Statistics
```bash
python manage.py setup_data --stats
```

### Create Manual Backup
```bash
python manage.py setup_data --backup
```

### Validate Data Integrity
```bash
python manage.py setup_data --validate
```

## Integration with Django Models

The JSON storage system works alongside Django models:
- **Automatic Sync**: Django model changes automatically sync to JSON
- **Middleware Integration**: Transparent data handling
- **Signal Handlers**: Automatic data synchronization on model saves
- **Backward Compatibility**: Existing Django functionality remains intact

## Performance Considerations

- **File-based Storage**: Fast read/write operations
- **User Isolation**: Separate files prevent conflicts
- **Efficient Indexing**: Index files for quick data access
- **Memory Management**: Optimized for large datasets

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure write permissions for data directory
2. **JSON Corruption**: Use validation command to check integrity
3. **Missing Files**: Run setup command to recreate structure
4. **Sync Issues**: Check middleware configuration

### Debug Commands

```bash
# Check data structure
ls -la data/

# Validate specific user data
python -c "from utils.json_storage import json_storage; print(json_storage.get_user_data(1))"

# Check storage statistics
python manage.py setup_data --stats
```

## Future Enhancements

- [ ] Data compression for large files
- [ ] Automatic cleanup of old activities
- [ ] Data export/import functionality
- [ ] Real-time data synchronization
- [ ] Advanced search capabilities
- [ ] Data analytics dashboard

---

**The JSON storage system is now fully integrated and ready for production use!**