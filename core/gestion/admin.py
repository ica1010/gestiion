from django.contrib import admin

from . models import Category, Product,Service,Fournisseur, Delivery,Supply, DeliveryProduct

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Service)
admin.site.register(Fournisseur)
admin.site.register(Delivery)
admin.site.register(DeliveryProduct)
admin.site.register(Supply)