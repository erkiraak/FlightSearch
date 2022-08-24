from django.shortcuts import render
from .models import Profile


def create_profile(request):
    """
    Creates a user profile from request user.
    :param request:
    :return:
    """
    Profile.objects.create(
        user=request.user,
        first_name=request.user.first_name,
        last_name=request.user.last_name,
        email=request.user.email
    )


def logged_in_view(request):
    if not Profile.objects.filter(user=request.user).exists():
        create_profile(request)
    return render(request, 'viewer/logged_in.html', {})


def login_view(request):
    return render(request, 'viewer/user.html', {})
