from django.shortcuts import render


def logged_in_view(request):
    return render(request, 'viewer/logged_in.html', {})


def login_view(request):
    return render(request, 'viewer/user.html', {})
