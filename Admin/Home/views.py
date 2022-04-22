from django.shortcuts import render
from core.Utils.Access.decorators import manager_required


@manager_required
def admin_index_view(request):
    return render(request, 'Admin/Home/index.html')
