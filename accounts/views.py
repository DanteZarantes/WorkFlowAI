from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .forms import SignUpForm, ProfileForm
from .models import UserProfile, UserActivity
from utils.json_storage import json_storage
import json

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.email = form.cleaned_data['email'].lower()
                user.save()
                
                # Create user profile
                UserProfile.objects.get_or_create(user=user)
                
                # Save user data to JSON and initialize empty data files
                try:
                    json_storage.save_user_data(user)
                    # Initialize empty data files for new user
                    json_storage.get_user_tasks(user.id)  # Creates empty tasks file
                    json_storage.get_user_projects(user.id)  # Creates empty projects file
                    json_storage.get_user_models(user.id)  # Creates empty models file
                    json_storage.update_user_activity(
                        user.id, 
                        'registration', 
                        'User account created',
                        {'ip_address': request.META.get('REMOTE_ADDR')}
                    )
                except Exception as e:
                    print(f"JSON storage error during registration: {e}")
                
                # Create activity record
                try:
                    UserActivity.objects.create(
                        user=user,
                        activity_type='login',
                        description='Account created and first login',
                        ip_address=request.META.get('REMOTE_ADDR'),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')
                    )
                except Exception as e:
                    print(f"Activity logging error: {e}")
                
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, 'Account created successfully!')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password.')
            return render(request, 'registration/login.html')
        
        # Try email authentication first
        user = authenticate(request, username=username, password=password)
        if not user:
            # Try with email as username
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None and user.is_active:
            login(request, user)
            
            # Update user data in JSON
            try:
                json_storage.save_user_data(user)
                json_storage.update_user_activity(
                    user.id,
                    'login',
                    'User logged in',
                    {'ip_address': request.META.get('REMOTE_ADDR')}
                )
            except Exception as e:
                print(f"JSON storage error: {e}")
            
            # Create activity record
            try:
                UserActivity.objects.create(
                    user=user,
                    activity_type='login',
                    description='User logged in',
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
            except Exception as e:
                print(f"Activity logging error: {e}")
            
            messages.success(request, 'Successfully logged in!')
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid credentials or account is disabled.')
    
    return render(request, 'registration/login.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            
            # Update user data in JSON
            json_storage.save_user_data(user)
            
            # Log profile update activity
            json_storage.update_user_activity(
                user.id,
                'profile_updated',
                'User profile updated'
            )
            
            # Create activity record
            UserActivity.objects.create(
                user=user,
                activity_type='profile_updated',
                description='Profile information updated',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})