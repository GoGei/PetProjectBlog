from django.shortcuts import render


def handler401_view(request, exception):
    return render(request, 'Admin/401.html', status=401)


def handler404_view(request, exception):
    return render(request, 'Admin/404.html', status=404)


def handler500_view(request, exception):
    return render(request, 'Admin/500.html', status=500)
