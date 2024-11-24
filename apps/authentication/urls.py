from django.urls import path
from apps.authentication import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('', views.index, name='index'),
    # path('billing/', views.billing, name='billing'),
    # path('tables/', views.tables, name='tables'),
    # path('vr/', views.vr, name='vr'),
    # path('rtl/', views.rtl, name='rtl'),
    # path('profile/', views.profile, name='profile'),

    # Authentication
    # path('login/', views.UserLoginView.as_view(), name='login'),
    path('login_auth/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path("register/choice_account/", views.choice_account, name="choice_account"),
    path(
        "register/account-activation/<uidb64>/<token>",
        views.activate,
        name="activate",
    ),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done"),
    path('auth/password-reset/', views.password_reset, name='password_reset'),
    path('auth/password_reset_link/<uidb64>/<token>/',
        views.reset_link, name='reset_link'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
