from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Film, Genre, Comment

# Register your models here.

admin.site.register(Film)
admin.site.register(Genre)
admin.site.register(Comment, MPTTModelAdmin)
