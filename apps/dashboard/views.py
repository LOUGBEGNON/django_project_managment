from lib2to3.fixes.fix_input import context

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url="/login_auth/")
def index(request):
    print(request.user)
    print("ndfjkbdgvbdjfvjdfnv")
    context = {

    }
    return render(request, "dashboard/index.html", context)


def billing(request):
  return render(request, 'dashboard/billing.html', { 'segment': 'billing' })

def tables(request):
  return render(request, 'dashboard/tables.html', { 'segment': 'tables' })

def vr(request):
  return render(request, 'dashboard/virtual-reality.html', { 'segment': 'vr' })

def rtl(request):
  return render(request, 'dashboard/rtl.html', { 'segment': 'rtl' })

def profile(request):
  return render(request, 'dashboard/profile.html', { 'segment': 'profile' })


