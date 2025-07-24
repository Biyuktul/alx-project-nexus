from django.db import models
<<<<<<< HEAD

# Create your models here.
=======
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

>>>>>>> release/1.0.0
