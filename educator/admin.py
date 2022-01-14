from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.EducatorDetail)
admin.site.register(models.Series)
admin.site.register(models.Lecture)
admin.site.register(models.Tag)
admin.site.register(models.Story)
