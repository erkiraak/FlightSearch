"""flightsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from search.views import search_view, DeleteAllSearch, ListSearch
from users.views import profile, edit_profile, delete_profile, \
    CreateProfilePageView
from subscription.views import (CreateSubscription,
                                ListSubscription,
                                UpdateSubscription,
                                DeleteSubscription,
                                DeleteAllSubscription
                                )

urlpatterns = [

    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', search_view, name='index'),
    path(
        'subscribe/<int:pk>',
        CreateSubscription.as_view(),
        name='create_subscription'
    ),
    path(
        'subscription/<int:pk>/edit',
        UpdateSubscription.as_view(),
        name='update_subscription'
    ),
    path(
        'subscription/<int:pk>/delete',
        DeleteSubscription.as_view(),
        name='delete_subscription'
    ),
    path(
        'subscriptions/delete',
        DeleteAllSubscription.as_view(),
        name='delete_all_subscription'
    ),
    path(
        'subscriptions/',
        ListSubscription.as_view(),
        name='list_subscription'
    ),
    path(
        'search_history/',
        ListSearch.as_view(),
        name='list_search',
    ),
    path(
        'search_history/delete',
        DeleteAllSearch.as_view(),
        name='delete_all_search'
    ),
    path(
        'profile/',
        profile,
        name='users-profile'
    ),
    path(
        'edit_profile/',
        edit_profile,
        name='users-edit_profile'
    ),
    path(
        'delete_account/', 
        delete_profile,
        name='users-delete_account'
    ),
    path(
        'create_profile_page/', 
        CreateProfilePageView.as_view(), 
        name='create_profile_page'
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
