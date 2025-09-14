from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def services(request):
    return render(request, 'core/services.html')

def contact(request):
    return render(request, 'core/contact.html')

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

def pricing(request):
    return render(request, 'core/pricing.html')

def blog(request):
    return render(request, 'core/blog.html')

def case_studies(request):
    return render(request, 'core/case_studies.html')

def resources(request):
    return render(request, 'core/resources.html')

def careers(request):
    return render(request, 'core/careers.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def terms(request):
    return render(request, 'core/terms.html')

def api_docs(request):
    return render(request, 'core/api_docs.html')

def tutorials(request):
    return render(request, 'core/tutorials.html')

def community(request):
    return render(request, 'core/community.html')

@login_required
def analytics(request):
    return render(request, 'core/analytics.html')

@login_required
def models(request):
    return render(request, 'core/models.html')

@login_required
def settings(request):
    return render(request, 'core/settings.html')

def team(request):
    return render(request, 'core/team.html')

def press(request):
    return render(request, 'core/press.html')

def machine_learning(request):
    return render(request, 'core/machine_learning.html')

def chatbots(request):
    return render(request, 'core/chatbots.html')

def computer_vision(request):
    return render(request, 'core/computer_vision.html')

def help_center(request):
    return render(request, 'core/help_center.html')

def ai_visualization(request):
    return render(request, 'core/ai_visualization.html')

def calculator(request):
    return render(request, 'core/calculator.html')

def text_analyzer(request):
    return render(request, 'core/text_analyzer.html')

def color_generator(request):
    return render(request, 'core/color_generator.html')

def user_directory(request):
    return render(request, 'core/user_directory.html')

def theme_settings(request):
    return render(request, 'core/theme_settings.html')