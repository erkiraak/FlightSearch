from django.urls import path
from .views import profile, edit_profile, delete_user

urlpatterns = [
    path('profile/', profile, name='users-profile'),
    path('edit_profile/', edit_profile, name='users-edit_profile'),
    path('delete_account/', delete_user, name='users-delete_account'),
]
