from django.db import models
from django.contrib.auth.models import AbstractUser


class Custom_user(AbstractUser):

    email = models.EmailField(blank=False, unique=True)




