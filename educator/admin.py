from django.contrib import admin
from . import models

class SereisAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

class EducatorDetailAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'educator')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'id', 'quiz', 'answer')

# Register your models here.
admin.site.register(models.EducatorDetail, EducatorDetailAdmin)
admin.site.register(models.Series, SereisAdmin)
admin.site.register(models.Lecture)
admin.site.register(models.Tag)
admin.site.register(models.Story)
admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Attachements)
