from django.contrib import admin
from .models import Photo, PhotoContext, Profile
# Register your models here.
admin.site.register(Photo)
admin.site.register(PhotoContext)
admin.site.register(Profile)