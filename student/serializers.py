from core.models import Notification
from core.serializers import UserViewSerializer as UserSerializer
from rest_framework.serializers import ModelSerializer
from .models import StudentDetail
from educator.models import Story
from educator.serializers import EducatorDetailSerializer

class StudentSerializer(ModelSerializer):
    class Meta:
        model = StudentDetail
        fields = '__all__'
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['student'] = UserSerializer(instance.student).data
        response['following'] = EducatorDetailSerializer(instance.following, many=True).data
        return response

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class StoryUserSerializer(ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'

    def to_representation(self, instance):
        response = {}
        response['educator'] = instance.educator.id
        response['name'] = instance.educator.name
        response['picture'] = instance.educator.educatordetail.picture
        return response
