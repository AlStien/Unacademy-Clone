# ------ imports -------
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import  MaxValueValidator, MinValueValidator
# core models
from core.models import User

from educator.models import Series, EducatorDetail, Question

class StudentDetail(models.Model):

    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    name = models.CharField(max_length=250)
    gender = models.CharField(max_length=20)
    birth = models.DateField(default='2004-01-01', null=True, blank=True)
    picture = models.CharField(max_length=700, null=True, blank=True)
    standard = models.CharField(max_length=20)       # all the credentials
    mobile = models.BigIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)], blank=True, null=True)
    bio = models.TextField(null=True, blank=True)

    wishlist = models.ManyToManyField(Series, related_name='wishlist', blank=True)
    following = models.ManyToManyField(EducatorDetail, related_name='educator_followers', blank=True)

    def __str__(self):
        return self.student.name

class Attempted(models.Model):
    student = models.ForeignKey(StudentDetail, on_delete=models.CASCADE, related_name='student_attempted')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_attempted')
    answer = models.IntegerField()
    is_correct = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self) -> str:
        return self.question.question

# class Score(models.Model):
#     quiz = models.ForeignKey()