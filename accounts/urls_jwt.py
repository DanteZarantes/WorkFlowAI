"""
JWT Authentication URLs
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import jwt_auth

urlpatterns = [
    path('api/auth/login/', jwt_auth.login_jwt, name='jwt_login'),
    path('api/auth/register/', jwt_auth.register_jwt, name='jwt_register'),
    path('api/auth/token/', jwt_auth.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]