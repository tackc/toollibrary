from django.contrib import admin
from .models import Tool, ToolRating, Profile, Category

# Register your models here.
admin.site.register(Tool)
admin.site.register(ToolRating)
admin.site.register(Profile)
admin.site.register(Category)