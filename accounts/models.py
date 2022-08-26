from tkinter import N
from django.db import models
from django.contrib.auth.models import AbstractUser


class Custom_user(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(blank = False, unique = True)
    rate = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "کاربران"


class User_info(models.Model):
    user = models.OneToOneField(Custom_user, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    address_1 = models.CharField(max_length = 128)
    address_2 = models.CharField(max_length = 128, blank = True)
    state = models.CharField(max_length = 64)
    city = models.CharField(max_length = 64)
    post_code = models.CharField(max_length = 10, null=False) 
    phone_number = models.CharField( max_length = 11)  

    def __str__(self):
        return f'info of {self.user}'

    class Meta:
        verbose_name_plural = "اطلاعات کاربران"


class Slider(models.Model):
    caption = models.CharField(max_length = 30)
    pic = models.ImageField(upload_to = 'slider_pics')
    state = models.CharField(max_length = 7)
    data_slide_to = models.IntegerField()

    class Meta:
        verbose_name_plural = "اسلایدر"
