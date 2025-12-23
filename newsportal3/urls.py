"""
URL configuration for newsportal3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from newsportal.views import ProtectedView, become_author
from newsportal.views import home
from newsportal import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ГЛАВНАЯ
    path('', home, name='home'),

    # НОВОСТИ
    path('news/', include('newsportal.urls')),

    # АВТОРИЗАЦИЯ
    path('accounts/', include('allauth.urls')),
    path('sign/', include('sign.urls')),

    # ЗАКРЫТАЯ СТРАНИЦА
    path('protected/', ProtectedView.as_view(), name='protected'),

    # ДЛЯ АВТОРА
    path('become-author/', become_author, name='become_author'),

    # АКТИВАЦИЯ АККАУНТА
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),

    # Redis
    path("", include("core.urls")),
]
