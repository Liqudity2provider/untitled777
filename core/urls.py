"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework_swagger.views import get_swagger_view

from users import views as user_views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt import views as jwt_views

from users.views import UserRegister, UserProfile
from rest_framework.schemas import get_schema_view

api_patterns = [
    path("api/users/", include("users.urls"), name="api-users"),
    # rest django jwt auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', include('rest_social_auth.urls_jwt_pair')),
    # blog urls
    path('', include('blog.urls')),

]

schema_view = get_swagger_view(title='Pastbin API', patterns=api_patterns)

urlpatterns = api_patterns + [
    path('admin/', admin.site.urls),

    # chat urls
    path('chat/', include('chat.urls')),

    # swagger url
    path('777', schema_view),

    # films url
    path('films/', include('films.urls')),

    # users urls
    path('register/', UserRegister.as_view(), name='register'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('login/', user_views.LoginView.as_view(), name='login'),
    path('logout/', user_views.LogoutView.as_view(), name='logout'),
]
