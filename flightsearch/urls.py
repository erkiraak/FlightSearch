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
from django.urls import path, include

from search.views import search_view
from users.views import profile
from viewer.views import login_view, logged_in_view
from subscription.views import (CreateSubscription,
                                ViewSubscription,
                                ListSubscription,
                                UpdateSubscription,
                                DeleteSubscription,
                                DeleteAllSubscription
                                )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('logged_in/', logged_in_view),
    path('', search_view, name='index'),
    path('subscribe/<int:pk>', CreateSubscription.as_view(), name='create_subscription'),
    path('subscription/<int:pk>', ViewSubscription.as_view(), name='view_subscription'),
    path('subscription/<int:pk>/edit', UpdateSubscription.as_view(), name='update_subscription'),
    path('subscription/<int:pk>/delete', DeleteSubscription.as_view(), name='delete_subscription'),
    path('subscriptions/delete', DeleteAllSubscription.as_view(), name='delete_all_subscription'),
    path('subscriptions', ListSubscription.as_view(), name='list_subscription'),
    path('profile/', profile, name='users-profile'),
]
