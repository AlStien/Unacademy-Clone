from django.contrib import admin
from . import models

admin.site.register(models.StudentDetail)
admin.site.register(models.Attempted)