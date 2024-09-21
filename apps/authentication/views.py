from django.shortcuts import render
import logging

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from apps.authentication.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, \
  UserPasswordChangeForm, RegisterForm
from django.contrib.auth import logout, login, update_session_auth_hash
from apps.authentication.backends import EmailAndSMSBackend, EmailBackend
import django.contrib.messages as messages
from django.conf import settings

from apps.utils import generate_username

logger = logging.getLogger("django")


# Create your views here.

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

    print("je suis ici")

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

      return redirect('/login_auth/')
    else:
      print("Register failed!")
  else:
    form = RegisterForm()

  context = { 'form': form }
  # return render(request, 'accounts/register.html', context)
  return render(request, 'authentication/register.html', context)

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm