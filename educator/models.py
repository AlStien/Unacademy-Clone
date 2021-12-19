# ------ imports -------
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import EmailValidator, MaxValueValidator, MinValueValidator

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, name, password, **other_fields):

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

        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):
        # other_fields.setdefault('is_verified', False)
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        name = name.strip().title()
        user = self.model(email=email, name=name, **other_fields)
        user.set_password(password)
        user.save()
        return user

# ------ User Model -------
class Educator(AbstractBaseUser, PermissionsMixin):


    # ------ Fields for Educator Profile -------
    email = models.EmailField(_('email address'), validators=[EmailValidator()], unique=True)
    name = models.CharField(max_length=150)
    
    # ------ Boolean Fields not to be accesed directly through User Profile -------
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_educator = models.BooleanField(default=False)

    # ------ Timestamp for user Created -------
    created = models.DateTimeField(auto_now_add=True)

    # ------ Account Manager for Custom User Model -------
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

class EducatorDetails(models.Model):
    # ------ Gender Choices -------
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )

    # ------ Course Choices -------
    COURSE_CHOICES = (
        ('J', 'IIT-JEE'),
        ('U', 'UPSC'),
        ('CP', 'COMPETITIVE PROGRAMMING')
    )

    educator = models.OneToOneField(Educator, on_delete=models.CASCADE)
    mobile = models.BigIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(60)], default=18)
    picture = models.ImageField(upload_to = 'educator/images')
    course = models.CharField(max_length=5, choices=COURSE_CHOICES)
    bio = models.TextField(blank=True)        # all the credentials and experieces to be mentioned in bio
    sample_video = models.FileField(upload_to='educator/sample-video', blank=True, null=True)
    # for ppts and other attachments to show with the sample video if any (optional)
    attachment = models.FileField(upload_to='educator/others', blank=True, null=True)

# ------ OTP Model -------
class OTP(models.Model):
    otp = models.IntegerField()
    otpEmail = models.EmailField()
    time_created = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.otp