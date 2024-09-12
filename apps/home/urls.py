# import notifications.urls
from django.conf import settings

# Includes for PWA URLs
from django.urls import include, path
# from pwa import views as pwaviews

from apps.home import views

urlpatterns = [
    # General links
    # The home page(s)
    # path("", views.index, name="default_home"),
    path("", views.index, name="index"),
    path("home/", views.index, name="default_home"),
    path("login/", views.index, name="default_home"),
]

