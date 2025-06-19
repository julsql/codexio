from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    current_collection = models.ForeignKey(
        'main.Collection',
        on_delete=models.PROTECT,
        related_name='current_users'
    )
