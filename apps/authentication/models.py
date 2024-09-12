import logging

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.fields import BooleanField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from django_cryptography.fields import encrypt
from phonenumber_field.modelfields import PhoneNumberField

logger = logging.getLogger("django")


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(
        self, username, first_login, email, phone_number, password, **extra_fields
    ):
        """Create and save a User with the given email and password."""

        if not email:
            raise ValueError("The email field must be defined")

        email = self.normalize_email(email)
        user = self.model(
            username=username,
            first_login=first_login,
            email=email,
            phone_number=phone_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(
        self, username, first_login, email, phone_number, password=None, **extra_fields
    ):
        """Create and save a regular User with the given email and password."""

        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)

        return self._create_user(
            username, first_login, email, password, phone_number, **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # question: do we need to handle the phone_number as for a normal user?
        return self._create_user(
            username=email,
            first_login=False,
            email=email,
            password=password,
            phone_number="",
            **extra_fields,
        )


class User(AbstractUser):
    """User model."""

    USER = 1
    MEMBER = 2
    STAFF = 3
    MANAGER = 4
    ADMIN = 4
    ROLE_CHOICES = (
        (USER, "USER"),
        (MEMBER, "MEMBER"),
        (STAFF, "STAFF"),
        (MANAGER, "MANAGER"),
        (ADMIN, "ADMIN"),
    )

    # username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = PhoneNumberField(_("phone number"), blank=True, max_length=128, region=None)
    first_login = BooleanField()
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    # code = models.IntegerField(null=True, blank=True)
    deactivation_date = models.DateTimeField(
        _("deactivation date"),
        blank=True,
        db_index=True,
        default=timezone.now,
        help_text=_("Deactivation date, by default it is now."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return "%s" % self.username

    def update_first_login(self):
        self.first_login = False
        self.save()
        return self

    # def is_member_of(self, municipality_slug):
    #     """Check if user is part of a given municipality's community"""
    #     try:
    #         slug = self.individual.municipality_slug
    #     except Exception as e:
    #         logger.error(e)
    #         slug = None
    #
    #     if slug == municipality_slug:
    #         return True
    #     else:
    #         return False
