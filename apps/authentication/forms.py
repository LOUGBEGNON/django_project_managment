
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, SetPasswordForm,
                                       UserCreationForm, UsernameField)
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from apps.authentication.models import User
from apps.dashboard.models import Company


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "autocomplete": "first_name",
                "class": "form-control",
            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "autocomplete": "last_name",
                "class": "form-control",
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "autocomplete": "email",
                "class": "form-control",
            }
        )
    )

    password1 = forms.CharField(
        label="Password", # Ajouter de champ pour changer password1 en password
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "autocomplete": "new-password",
                "class": "form-control",
            }
        )
    )

    password2 = forms.CharField(
        label="Confirmation Password",  # Changement ici
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "autocomplete": "new-password",
                "class": "form-control",
            }
        )
    )

    # We disable the captcha for the Sign Up form
    # captcha = CaptchaField(widget=CustomCaptchaTextInput)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password1", "password2", )


class UpdateCompanyForm(forms.ModelForm):
    social_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Company Social name",
                "autocomplete": "name",
            },
        )
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Company name",
                "autocomplete": "name",
            },
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "autocomplete": "email",
                "class": "form-control",
            }
        )
    )

    address = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Company address",
                "autocomplete": "address",
            },
        )
    )

    class Meta:
        model = Company
        fields = [
            "social_name",
            "name",
            "email",
            "address",
        ]


# class RegistrationForm(UserCreationForm):
#   password1= forms.CharField(
#       label=_("Password"),
#       widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
#   )
#   password2 = forms.CharField(
#       label=_("Password Confirmation"),
#       widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirmation'}),
#   )
#
#   class Meta:
#     model = User
#     fields = ('username', 'email', )
#
#     widgets = {
#       'username': forms.TextInput(attrs={
#           'class': 'form-control',
#           'placeholder': 'Username'
#       }),
#       'email': forms.EmailInput(attrs={
#           'class': 'form-control',
#           'placeholder': 'Email'
#       })
#     }


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "autocomplete": "email",
                "class": "form-control",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "autocomplete": "current-password",
                "class": "form-control",
            }
        )
    )
    # captcha = CaptchaField(widget=CustomCaptchaTextInput)




 #class LoginForm(AuthenticationForm):
   #username = UsernameField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}))
  #password = forms.CharField(
     #  label=_("Password"),
      #strip=False,
     # widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
#)

class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "autocomplete": "email",
                "class": "form-control",
            }
        )
    )

class UserPasswordResetForm(SetPasswordForm):
    """Change password form."""

    new_password1 = forms.CharField(
        label="Password",
        help_text="<ul class='errorlist text-muted'><li>Your password can 't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can 't be a commonly used password.</li> <li>Your password can 't be entirely numeric.<li></ul>",
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "password",
                "type": "password",
                "id": "user_password",
            }
        ),
    )

    new_password2 = forms.CharField(
        label="Confirm password",
        help_text=False,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "confirm password",
                "type": "password",
                "id": "user_password",
            }
        ),
    )


'''
class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")
    

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Old Password'
    }), label='Old Password')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")
    '''
class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Old Password'
    }), label='Old Password')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'New Password'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirm New Password'
    }), label="Confirm New Password")

