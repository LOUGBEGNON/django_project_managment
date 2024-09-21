# import notifications.urls
from django.conf import settings

# Includes for PWA URLs
from django.urls import include, path
# from pwa import views as pwaviews

from apps.dashboard import views

urlpatterns = [
    # General links
    # The home page(s)
    # path("", views.index, name="default_home"),
    path("dashboard/", views.index, name="home"),
    path('billing/', views.billing, name='billing'),
    path('tables/', views.tables, name='tables'),
    path('vr/', views.vr, name='vr'),
    path('rtl/', views.rtl, name='rtl'),
    path('profile/', views.profile, name='profile'),
]

