from core.models import User
from core.serializers import UserViewSerializer as UserSerializer
from rest_framework.serializers import ModelSerializer
from .models import StudentDetail

class StudentSerializer(ModelSerializer):
    class Meta:
        model = StudentDetail
        fields = '__all__'
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['student'] = UserSerializer(instance.student).data
        return response
