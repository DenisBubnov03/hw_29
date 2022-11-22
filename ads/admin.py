from django.contrib import admin

from ads.models import Category, Ad

# Register your models here.
admin.site.register(Ad)
admin.site.register(Category)