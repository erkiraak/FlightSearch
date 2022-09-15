from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UpdateUserForm, UpdateProfileForm, ProfileDeleteForm


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES,
                                         instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
def delete_profile(request):
    if request.method == 'POST':
        delete_form = ProfileDeleteForm(request.POST, instance=request.user.profile)
        user = request.user.profile
        user.delete()
        messages.info(request, 'Your account has been deleted.')
        return redirect('index')
    else:
        delete_form = ProfileDeleteForm(instance=request.user.profile)

    context = {
        'delete_form': delete_form
    }

    return render(request, 'delete_account.html', context)
