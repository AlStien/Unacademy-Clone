from .models import EducatorDetail, Lecture, Series, Story
from core.models import User
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'is_educator', 'is_student']

class EducatorDetailSerializer(ModelSerializer):
    class Meta:
        model = EducatorDetail
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['educator'] = UserSerializer(instance.educator).data
        return response

class SeriesSerializer(ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'
            
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['educator details']=EducatorDetailSerializer(instance.educator.educatordetail).data
        return response

class LectureSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        series = Series.objects.get(id = instance.series.id)
        response.pop('series')
        response['series name']=series.name
        response['series description']=series.description
        response['series icon']=series.icon
        return response

class StorySerializer(ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'
