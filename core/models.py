from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's built-in AbstractUser.

    This allows for additional user fields to be added if needed in the future
    while maintaining compatibility with Django's authentication system.
    No additional fields are currently defined, but the class is set up
    to facilitate future expansion.
    """

    pass
