from django.db.models.signals import post_save

from core.models import Notification, User
from .models import StudentDetail
from educator.models import Lecture

def new_upload(*args, **kwargs):
    print(kwargs)
    series = kwargs['instance'].series
    user = kwargs['instance'].series.educator
    followers = []
    for f in StudentDetail.objects.filter(following = user.educatordetail.id):
        f = User.objects.get(email = f.student.email)
        followers.append(f)
    print(followers)
    followers = [Notification(
            receiver = student, sender = user,
            subject = f'New Lecture Uplaod',
            message=f"{user} has uploaded a new video in {series}."
        ) for student in followers]
    Notification.objects.bulk_create(followers)
post_save.connect(new_upload, sender = Lecture)