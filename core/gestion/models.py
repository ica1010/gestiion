from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauth.models import SupplierProfile, AdminProfile , User
# Create your models here.


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length= 20 , alphabet='abcdefghijklmnopqrstuvwxyz1234567890' , editable=False,  prefix='Cat-')
    title = models.CharField(max_length=100, default='untitle category')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length= 20 , alphabet='abcdefghijklmnopqrstuvwxyz1234567890' , editable=False,  prefix='Prod-')
    title = models.CharField(max_length=100, default='untitle product')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL , null=True , related_name='category')
    
    quantity = models.PositiveIntegerField()

    description = models.TextField()
    # short_description = models.CharField(max_length=100, default='')
    # keywords = models.CharField(max_length=100, default='')

    image = models.ImageField(default="./new-document.png", null = False,blank= False, upload_to='product_image' )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Service(models.Model):
    sid = ShortUUIDField(unique=True, length=10, max_length= 20 , alphabet='abcdefghijklmnopqrstuvwxyz1234567890' , editable=False,  prefix='Service-')
    title = models.CharField(max_length=100, default='untitle service')

    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title    

class Fournisseur(models.Model):
    fid = ShortUUIDField(unique=True, length=10, max_length= 20 , alphabet='abcdefghijklmnopqrstuvwxyz1234567890' , editable=False,  prefix='Fourn-')
    title = models.CharField(max_length=100, default='untitle fournisseur')

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Delivery(models.Model):
    did = ShortUUIDField(unique=True, length=10, max_length= 20 , alphabet='abcdefghijklmnopqrstuvwxyz1234567890' , editable=False,  prefix='Del-')
    user = models.ForeignKey(User, on_delete=models.SET_NULL , null=True , blank=True)
    post = models.CharField(max_length=200)
    service = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.did
    
class DeliveryProduct(models.Model):
    #dpid = ShortUUIDField(unique=True, length=10, max_length= 20 , alphabet='abcdefghijklmnopqrstuvwxyz1234567890' , editable=False,  prefix='DelProd-')
    delivery = models.ForeignKey(Delivery,on_delete=models.SET_NULL , null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return self.product.title
    
class Supply(models.Model):
    sid = ShortUUIDField(unique=True, length=10, max_length= 20 , alphabet='abcdefghijklmnopqrstuvwxyz1234567890' , editable=False,  prefix='Sup-')
    user = models.ForeignKey(User, on_delete=models.SET_NULL , null=True , blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    fournisseur = models.ForeignKey(Fournisseur, verbose_name=("Fournisseur"), on_delete=models.SET_NULL,blank=True, null=True)
    livrer_name = models.CharField(max_length=500, default='not set')
    livrer_phone = models.CharField(max_length=500, default='not set')
    detail = models.TextField(blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


class Action(models.Model):
    aid = ShortUUIDField(unique=True, length=10, max_length= 20 , alphabet='abcdefghijklmnopqrstuvwxyz1234567890' , editable=False,  prefix='Action-')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.TextField()
    private = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 