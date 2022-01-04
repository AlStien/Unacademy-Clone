from .models import EducatorDetail, Series
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
        response['educator'] = UserSerializer(instance.educator).data
        return response
