from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str as force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from apps.authentication.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, \
  UserPasswordChangeForm, RegisterForm
from django.contrib.auth import logout, login, update_session_auth_hash, get_user_model
from apps.authentication.backends import EmailBackend
import django.contrib.messages as messages
from django.conf import settings
from apps.authentication.models import User
from apps.authentication.tokens import account_activation_token
from apps.utils import generate_username

logger = logging.getLogger("django")


# Pages
def index(request):

  return render(request, 'pages/index.html', { 'segment': 'index' })

def billing(request):
  return render(request, 'pages/billing.html', { 'segment': 'billing' })

def tables(request):
  return render(request, 'pages/tables.html', { 'segment': 'tables' })

def vr(request):
  return render(request, 'pages/virtual-reality.html', { 'segment': 'vr' })

def rtl(request):
  return render(request, 'pages/rtl.html', { 'segment': 'rtl' })

def profile(request):
  return render(request, 'pages/profile.html', { 'segment': 'profile' })


# Authentication
# class UserLoginView(LoginView):
#   print("nhdfjvb fbgdvg")
#   template_name = 'accounts/login.html'
#   form_class = LoginForm

def login_view(request):
    """Login page, only an anonymous user.
    Already logged-in users that are also Individual get redirected to the right page.
    """

    if hasattr(request.user, "individual") and request.user.is_authenticated:
      return redirect(
        "home", municipality_slug=request.user.individual.municipality_slug
      )

    form = LoginForm(request.POST or None)
    msg, municipality = "", None

    if form.is_valid():
      email = form.cleaned_data.get("email")
      password = form.cleaned_data.get("password")
      print(email)
      print(password)

      email_backend = EmailBackend()
      user = email_backend.authenticate(request, username=email, password=password)

      if user is not None:
        login(request, user, backend="apps.authentication.backends.EmailBackend")
        if user.is_active:
          print(user)
          # add the user to the default group(s), if needed
          # For "individuals", we add them to the community group
          # if hasattr(user, "individual"):
          #   # if request.user.individual.municipality:
          #   #   municipality = Municipality.objects.get(
          #   #     slug=request.user.individual.municipality_slug
          #   #   )
          #   # else:
          #   #   if user.role == user.INDIVIDUAL:
          #   #     return redirect("inactive_account")
          #   #   return redirect("register_municipality")
          #   #
          #   # if user.role == user.INDIVIDUAL:
          #   #   if not user.groups.filter(
          #   #           name=settings.COMMUNITY_GROUP
          #   #   ).exists():
          #   #     grp = Group.objects.get(name=settings.COMMUNITY_GROUP)
          #   #     grp.user_set.add(user)
          #   #   return redirect(
          #   #     reverse(
          #   #       "home",
          #   #       kwargs={"municipality_slug": municipality.slug},
          #   #     )
          #   #   )
          #   # elif user.role == user.MUNICIPALITY:
          #   #   return redirect(
          #   #     reverse(
          #   #       "home",
          #   #       kwargs={"municipality_slug": municipality.slug},
          #   #     )
          #   #   )
          #   # elif user.role == user.COMPANY:
          #   #   return redirect(
          #   #     reverse(
          #   #       "home",
          #   #       kwargs={"municipality_slug": municipality.slug},
          #   #     )
          #   #   )
          #   pass
          # else:
          #   return redirect("register_individual")
          print("Je suis bien connecté et je suis redirigé")
          return redirect("home")
        else:
          msg = "Please confirm your email before logging in."
          messages.error(request, msg)
        return redirect("home")
      else:
        msg = "Please confirm your email before logging in."
        messages.error(request, msg)
    else:
      print(form.errors)
      if request.method == "POST":
        msg = "We couldn't validate your email. Please try again."
        messages.error(request, msg)

    return render(request, "authentication/login.html", {"form": form, "msg": msg})


# @redir_if_authenticated(redir_url_name="home")
def choice_account(request):
    return render(request, "authentication/choice_account.html")


def register(request):
  msg = None
  success = False

  if "type_account" in request.GET:
    type_account = request.GET.get("type_account")
  else:
    type_account = "user"

  print(type_account)

  if request.method == 'POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
      # form.save()
      user = form.save(commit=False)
      user.is_active = False
      user.first_login = True

      to_email = form.cleaned_data.get("email")

      if type_account == "member":
        user.role = user.MEMBER
      elif type_account == "staff":
        user.role = user.STAFF
      elif type_account == "manager":
        user.role = user.MANAGER

      user.username = generate_username(to_email)

      user.save()
      print('Account created successfully!')
      logger.info(f"User model {user.id} saved")

      login(request, user, backend="apps.authentication.backends.EmailBackend")

      # Send verification mail. Handle any exception that could occur.
      try:
        verify_email(user, request)
        logger.info(f"Send verification email for {user.username}")
        logger.info(f"Send New User {user.username} notification to Project...")

        send_mail(
          user.username + " registered to Project",
          "A new user ("
          + user.username
          + ") with email "
          + " has registered to Project Managemant",
          "amedeelougbegnon3@gmail.com",
          ['lougbegnona@gmail.com'],
          fail_silently=False,
        )

        return redirect('/login_auth/')
      except Exception as e:
        print(e)
        msg = settings.ERROR_COULD_NOT_SEND_VERIF_EMAIL
        messages.error(request, msg)
        logger.error(f"Error sending the verification message: {e}")


    else:
      print("Register failed!")
  else:
    form = RegisterForm()

  context = {
    'form': form,
    "msg": msg,
    "success": success
  }
  # return render(request, 'accounts/register.html', context)
  return render(request, 'authentication/register.html', context)

def activate(request, uidb64, token):
    response = None
    try:
      uid = force_text(urlsafe_base64_decode(uidb64))
      user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
      user = None
    if user is not None and account_activation_token.check_token(user, token):
      user.is_active = True
      user.save()
      response = "Thank you for confirming your email. Your account has been activated."
    return render(
      request,
      "authentication/account_activation_status.html",
      {"response": response},
    )


def verify_email(user, request):
    """Send verification mail"""
    # from apps.authentication.views.utils import get_site_scheme_and_domain

    site_domain = get_current_site(request)

    from_email = (
            "Project Management <" + "amedeelougbegnon3@gmail.com" + ">"
    )
    mail_subject = "Account Registration Confirmation"
    to_email = user.email

    msge = render_to_string(
      "authentication/acc_active_email.txt",
      {
        "username": user.username,
        "url": reverse(
          "activate",
          kwargs={
            "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
          },
        ),
        "domain": site_domain,
        "scheme": "http",
      },
    )

    msge_html = render_to_string(
      "authentication/acc_active_email.html",
      {
        "username": user.username,
        "url": reverse(
          "activate",
          kwargs={
            "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
          },
        ),
        "domain": site_domain,
        "scheme": "http",
      },
    )
    send_mail(
      mail_subject,
      msge,
      from_email,
      [to_email],
      fail_silently=False,
      html_message=msge_html,
    )


def logout_view(request):
  logout(request)
  return redirect('/login/')

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm


