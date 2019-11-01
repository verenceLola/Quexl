from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Service, Category, Order, Request, Payment

admin.site.register(Service)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(Request)
admin.site.register(Category, MPTTModelAdmin)
