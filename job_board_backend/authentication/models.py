from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_recruiter = models.BooleanField(default=False)
