from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Category
from .models import Service

admin.site.register(Service)
admin.site.register(Category, MPTTModelAdmin)
