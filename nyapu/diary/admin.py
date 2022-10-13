from django.contrib import admin

# Register your models here.
from .models import Diary, Like, Comment

admin.site.register(Diary)
admin.site.register(Like)
admin.site.register(Comment)
