from django.shortcuts import render, redirect
from django_hosts import reverse
from django.contrib.auth import authenticate, login, logout

from core.Utils.Access.decorators import manager_required
from .forms import LoginForm


def admin_login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        user = authenticate(username=cleaned_data['email'], password=cleaned_data['password'])
        if user:
            if user.is_active and user.is_staff:
                login(request, user)
                return redirect(reverse('admin-index', host='admin'))
            elif not user.is_staff or not user.is_superuser:
                form.add_error(None, 'User is not staff')
            else:
                form.add_error(None, 'User is inactive')
        else:
            form.add_error(None, "Please enter a correct email and password.")

    return render(request, 'Admin/Login/login.html',
                  {'form': form})


@manager_required
def admin_logout_view(request):
    logout(request)
    return redirect(reverse('admin-login', host='admin'))
