from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'home/home.html')


def error_404(request):
    return render(request, 'home/404.html')