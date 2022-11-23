from django.contrib import admin

from users.models import Location, User

# Register your models here.
admin.site.register(User)
admin.site.register(Location)
