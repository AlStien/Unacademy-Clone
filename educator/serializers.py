from .models import EducatorDetail, Series
from core.models import User
from rest_framework.serializers import ModelSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'is_educator', 'is_student']

class EducatorDetailSerializer(ModelSerializer):
    educator = UserSerializer()
    class Meta:
        model = EducatorDetail
        fields = '__all__'

class SeriesSerializer(ModelSerializer):
    educator = UserSerializer()
    class Meta:
        model = Series
        fields = '__all__'