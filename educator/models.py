# ------ imports -------
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import  MaxValueValidator, MinValueValidator
# core models
from core.models import User as Educator

class EducatorDetail(models.Model):
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
