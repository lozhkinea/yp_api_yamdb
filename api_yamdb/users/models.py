from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

ROLE_CHOICES = [
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
]


class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(_('biography'), blank=True)
    role = models.CharField(
        _('user role'), max_length=9, choices=ROLE_CHOICES, default='user'
    )

    @property
    def is_admin(self):
        return self.is_staff or self.role in ['admin']

    @property
    def is_moderator(self):
        return self.is_admin or self.role in ['moderator']

    @property
    def is_user(self):
        return self.role in ['user']
