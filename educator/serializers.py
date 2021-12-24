from .models import EducatorDetail
from rest_framework.serializers import ModelSerializer

class EducatorDetailSerializer(ModelSerializer):
    class Meta:
        model = EducatorDetail
        fields = '__all__'