"""siriusbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

import mainapp
from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get_all_categories/', mainapp.views.get_all_categories),
    path('get_user_info/', mainapp.views.get_user_info),
    path('get_user_interests/', mainapp.views.get_user_interests),
    path('get_user_events/', mainapp.views.get_user_events),
    path('get_organizer_info/', mainapp.views.get_organizer_info),
    path("get_event/", mainapp.views.get_event_info),
    path("get_event_by_id/", mainapp.views.get_event_by_id),
    path("subscribe/", mainapp.views.subscribe),
    path("get_events/", mainapp.views.get_events),

    path("register/", mainapp.views.register_user),

    path("add_event/", mainapp.views.add_event),

    path("add_rating/", mainapp.views.rating)
]
