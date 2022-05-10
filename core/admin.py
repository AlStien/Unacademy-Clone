from django.contrib import admin
from . import models

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'id', 'name', 'is_verified', 'is_educator', 'is_student')

class OTPAdmin(admin.ModelAdmin):
    list_display = ('otpEmail', 'otp', 'time_created')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'subject', 'message', 'is_seen')

# Register your models here.
admin.site.register(models.User, UserAdmin)
admin.site.register(models.OTP, OTPAdmin)
admin.site.register(models.Notification, NotificationAdmin)