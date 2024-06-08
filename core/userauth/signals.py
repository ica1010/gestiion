from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, SupplierProfile, AdminProfile
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

@receiver(post_save, sender=User)
def create_supplier_profile(sender, instance, created, **kwargs):
    if created and instance.is_supplier:
        SupplierProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_admin_profile(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        AdminProfile.objects.create(user=instance)
