from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Service, Category

admin.site.register(Service)
admin.site.register(Category, MPTTModelAdmin)
