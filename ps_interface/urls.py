"""
URL configuration for ps_interface project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from ps_interface import views

handler403 = views.PermissionDeniedView.as_view()

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", view=views.index, name="index"),
    path("harvester/", include("ps_harvester.urls"), name="ps_harvester"),
    path("auth/", include("ps_auth.urls"), name="auth"),
    path("users/", include("ps_users.urls"), name="users"),
]
