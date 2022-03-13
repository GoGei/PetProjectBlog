from django.shortcuts import render, redirect
from django_hosts import reverse
from core.Utils.Access.decorators import manager_required


def admin_login_view(request):
    return render(request, 'Admin/Login/login.html')


@manager_required()
def admin_logout_view(request):
    return redirect(reverse('admin-login', host='admin'))
