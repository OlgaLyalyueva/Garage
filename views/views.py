from django.shortcuts import render


def main_view(request):
    return render(request, 'Garage/main.html')


def about(request):
    return render(request, 'Garage/about_us.html')
