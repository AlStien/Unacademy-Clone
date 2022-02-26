from core.models import Notification
from .models import EducatorDetail, Lecture, Question, Quiz, Series, Story
from student.models import StudentDetail
from core.models import User
from core.serializers import UserViewSerializer as UserSerializer
from rest_framework.serializers import ModelSerializer


class EducatorDetailSerializer(ModelSerializer):
    class Meta:
        model = EducatorDetail
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['educator'] = UserSerializer(instance.educator).data
        response['educator_series'] = SeriesSerializer(Series.objects.filter(educator = instance.educator), many=True).data
        response['educator_quiz'] = QuizSerializer(Quiz.objects.filter(educator = instance.educator), many=True).data
        return response

class SeriesSerializer(ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'

class LectureSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        series = Series.objects.get(id = instance.series.id)
        response.pop('series')
        response['series_name']=series.name
        response['series_description']=series.description
        response['series_icon']=series.icon
        return response

class StorySerializer(ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'

    def to_representation(self, instance):
        response = {}
        response['doc'] = instance.doc
        response['educator'] = instance.educator.name
        return response

class QuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class AnnouncementSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'