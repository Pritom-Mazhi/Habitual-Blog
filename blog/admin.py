from django.contrib import admin

# Register your models here.
from .models import BlogPost #, Blog

admin.site.register(BlogPost)
# admin.site.register(Blog)
