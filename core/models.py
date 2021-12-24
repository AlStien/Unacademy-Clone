# ------ imports -------
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import EmailValidator

# user manager for custom user model
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_verified', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password=None, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        # name = name.strip().title()
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

# ------ User Model -------
class User(AbstractBaseUser, PermissionsMixin):


    # ------ Fields for Profile -------
    email = models.EmailField(_('email address'), validators=[EmailValidator()], unique=True)
    name = models.CharField(max_length=150)
    
    # ------ Boolean Fields not to be accesed directly through User Profile -------
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_educator = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    # ------ Timestamp for user Created -------
    created = models.DateTimeField(auto_now_add=True)

    # ------ Account Manager for Custom User Model -------
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


# ------ OTP Model -------
class OTP(models.Model):
    otp = models.IntegerField()
    otpEmail = models.EmailField()
    time_created = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.otpEmail}: {self.otp}'