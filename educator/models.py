# ------ imports -------
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import  MaxValueValidator, MinValueValidator
# core models
from core.models import User

class EducatorDetail(models.Model):

    educator = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True)
    mobile = models.BigIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    gender = models.CharField(max_length=20)
    birth = models.DateField(default='2004-01-01')
    picture = models.CharField(max_length=250)
    qual = models.TextField(null=True)       # all the credentials
    bio = models.TextField(blank=True, null=True)        # experieces to be mentioned in bio
    sample_video = models.CharField(max_length=250, blank=True, null=True)
    # for ppts and other attachments to show with the sample video if any (optional)
    attachment = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.educator.name

# Educator first needs to create a lecture series to upload lectures
class Series(models.Model):
    educator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educator_name')
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(default='This Series is about ....')
    icon = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.name

# Model for Lectures to be uploaded in a series
class Lecture(models.Model):
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='series_name')
    name = models.CharField(max_length=200)
    video = models.CharField(max_length=250)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name

# ------ Tags for Products -------
class Tag(models.Model):
    # a product can have many tags so many-to-one relationship
    lecture = models.ManyToManyField(Lecture, related_name="lecture_name")
    tag = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.tag
