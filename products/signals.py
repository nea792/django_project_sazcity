from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Custom_user
from .models import Cart


@receiver(post_save, sender=Custom_user)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


@receiver(post_save, sender=Custom_user)
def save_profile(sender, instance, **kwargs):
        instance.Cart.save()
 