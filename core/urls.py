"""
Core Application URL Configuration

This file defines URL patterns for the main NeuralFlow application.
Includes routes for:
- Public pages (home, about, services, pricing)
- AI tools (calculator, text analyzer, color generator)
- User dashboard and management pages
- Help and community pages

All URLs are relative to the root domain (e.g., http://localhost:8000/)
"""

from django.urls import path
from . import views

# URL patterns for core application
urlpatterns = [
    # Main Pages
    path('', views.home, name='home'),                           # Homepage
    path('about/', views.about, name='about'),                   # About Us
    path('services/', views.services, name='services'),         # AI Services
    path('contact/', views.contact, name='contact'),             # Contact Form
    path('pricing/', views.pricing, name='pricing'),             # Pricing Plans
    
    # User Dashboard (requires login)
    path('dashboard/', views.dashboard, name='dashboard'),       # User Dashboard
    
    # Content & Resources
    path('blog/', views.blog, name='blog'),                      # Blog Posts
    path('case-studies/', views.case_studies, name='case_studies'), # Case Studies
    path('resources/', views.resources, name='resources'),       # Resources Hub
    path('tutorials/', views.tutorials, name='tutorials'),       # Learning Tutorials
    path('api-docs/', views.api_docs, name='api_docs'),         # API Documentation
    path('community/', views.community, name='community'),       # Community Hub
    path('help/', views.help_center, name='help_center'),       # Help Center
    
    # Company Pages
    path('careers/', views.careers, name='careers'),             # Job Openings
    path('team/', views.team, name='team'),                     # Team Members
    path('press/', views.press, name='press'),                  # Press & Media
    path('privacy/', views.privacy, name='privacy'),             # Privacy Policy
    path('terms/', views.terms, name='terms'),                  # Terms of Service
    
    # AI Services & Tools
    path('machine-learning/', views.machine_learning, name='machine_learning'), # ML Platform
    path('chatbots/', views.chatbots, name='chatbots'),         # Chatbot Builder
    path('computer-vision/', views.computer_vision, name='computer_vision'), # Computer Vision
    path('ai-visualization/', views.ai_visualization, name='ai_visualization'), # 3D Visualization
    
    # Interactive Tools
    path('calculator/', views.calculator, name='calculator'),    # Cost Calculator
    path('text-analyzer/', views.text_analyzer, name='text_analyzer'), # Text Analysis
    path('color-generator/', views.color_generator, name='color_generator'), # Color Palette
    
    # Project Management
    path('project-boards/', views.project_boards, name='project_boards'), # AI Project Boards
    path('ai-tools/mindmap/', views.mindmap, name='mindmap'),    # Mind Map Tool
    path('ai-tools/task-tree/', views.task_tree, name='task_tree'), # Task Tree Tool
    path('ai-tools/kanban/', views.kanban, name='kanban'),       # Kanban Board
    path('ai-tools/dashboard/', views.ai_dashboard, name='ai_dashboard'), # AI Dashboard
    
    # User Features (requires login)
    path('analytics/', views.analytics, name='analytics'),       # Usage Analytics
    path('models/', views.models, name='models'),               # AI Models Management
    path('settings/', views.settings, name='settings'),         # Account Settings
    path('user-directory/', views.user_directory, name='user_directory'), # Find Users
    path('theme-settings/', views.theme_settings, name='theme_settings'), # Theme Customization
]