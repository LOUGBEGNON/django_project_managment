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
    path("dashboard/view_project/<int:id>/", views.view_project, name="view_project"),
    path("dashboard/view_project/start_task/<int:id>/", views.start_task, name="start_task"),
    path("dashboard/view_project/pause_task/<int:id>/", views.pause_task, name="pause_task"),
    path("dashboard/view_project/complete_task/<int:id>/", views.complete_task, name="complete_task"),
    path("dashboard/view_diagram/", views.task_gantt_chart, name="view_diagram"),
    path("dashboard/anychart/", views.anychart_gantt, name="anychart"),
    path("dashboard/projects/", views.projects, name="projects"),
    path('billing/', views.billing, name='billing'),
    path('tables/', views.tables, name='tables'),
    path('vr/', views.vr, name='vr'),
    path('rtl/', views.rtl, name='rtl'),
    path('profile/', views.profile, name='profile'),
]

