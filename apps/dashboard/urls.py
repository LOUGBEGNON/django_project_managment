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
    path("dashboard/create_company", views.create_company, name="create_company"),
    path("dashboard/project/update/<int:id>/", views.update_project, name="update_project"),
    path("dashboard/view_project/<int:id>/", views.view_project, name="view_project"),
    path("dashboard/send_mail_app/", views.send_mail_app, name="send_mail_app"),
    path("dashboard/view_task/<int:id>/", views.view_task, name="view_task"),
    path("dashboard/view_project/start_task/<int:id>/", views.start_task, name="start_task"),
    path("dashboard/view_project/update_assignation/<int:id>/", views.update_assignation, name="update_assignation"),
    path("dashboard/view_project/pause_task/<int:id>/", views.pause_task, name="pause_task"),
    path("dashboard/view_project/complete_task/<int:id>/", views.complete_task, name="complete_task"),
    path("dashboard/view_diagram/", views.task_gantt_chart, name="view_diagram"),
    path("dashboard/anychart/", views.anychart_gantt, name="anychart"),
    path("dashboard/projects/", views.projects, name="projects"),
    path("dashboard/my_tasks/", views.my_tasks, name="my_tasks"),
    path('billing/', views.billing, name='billing'),
    path('tables/', views.tables, name='tables'),
    path('vr/', views.vr, name='vr'),
    path('rtl/', views.rtl, name='rtl'),
    path('profile/', views.profile, name='profile'),
    path('company/profile/<int:id>', views.company_profile, name='company_profile'),
    # path('company/update', views.update_company, name='update_company'),
    path('company/invite/<int:id>/', views.invite_company, name='invite_company'),
    path(
        "company/invite/acceptation/<int:company_id>",
        views.acceptation_invitation_new_user,
        name="acceptation_invitation_new_user",
    ),
]

