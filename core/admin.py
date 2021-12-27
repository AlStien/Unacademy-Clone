from django.contrib import admin
from . import models

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_verified', 'is_educator', 'is_student')

class OTPAdmin(admin.ModelAdmin):
    list_display = ('otpEmail', 'otp', 'time_created')
# Register your models here.
admin.site.register(models.User, UserAdmin)
admin.site.register(models.OTP, OTPAdmin)