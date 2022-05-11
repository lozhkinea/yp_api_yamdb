from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True, blank=True)
    bio = models.TextField(_("biography"), blank=True)
    role = models.CharField(_("user role"), max_length=150)
