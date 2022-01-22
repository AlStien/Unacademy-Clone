from django.contrib import admin
from . import models

class SereisAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

# Register your models here.
admin.site.register(models.EducatorDetail)
admin.site.register(models.Series, SereisAdmin)
admin.site.register(models.Lecture)
admin.site.register(models.Tag)
admin.site.register(models.Story)
