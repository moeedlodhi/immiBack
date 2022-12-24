"""immigrationback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from authentication import views
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    path('authtoken/', views.AuthJsonWebTokeView.as_view(), name='authtoken'),
    path('login/', views.loginuser.as_view(), name='login'),
    path('verify/', views.verifyToken.as_view(), name='verify'),
    path('api-token-refresh/', refresh_jwt_token)
]
