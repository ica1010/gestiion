from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from django.contrib.auth.models import Group, Permission , User

class User(AbstractUser):
    id= ShortUUIDField(unique=True, length=4, max_length= 20 ,prefix='', alphabet='1234567890',primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=60, unique=True)
    image= models.ImageField(default="./default.jpg")
    phone = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username
        
class SupplierProfile(models.Model):
    sid = ShortUUIDField(unique=True, max_length=20, primary_key=True  , editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    # Ajoutez d'autres champs spécifiques au fournisseur si nécessaire

    def __str__(self):
        return str(self.user)

class AdminProfile(models.Model):
    aid = ShortUUIDField(unique=True, max_length=20, primary_key=True,editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    # Ajoutez d'autres champs spécifiques à l'administrateur si nécessaire
    def __str__(self):
        return str(self.user)
    

User.groups.field.remote_field.related_name = 'user_groups'
User.user_permissions.field.remote_field.related_name = 'user_permissions'
Group.user_set.field.remote_field.related_name = 'group_users'
Permission.user_set.field.remote_field.related_name = 'permission_users'