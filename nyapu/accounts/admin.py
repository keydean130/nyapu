from django.contrib import admin
from .models import CustomUser, Relationship

admin.site.register(CustomUser)
admin.site.register(Relationship)
