from educator.models import Question
from core.models import Notification
from core.serializers import UserViewSerializer as UserSerializer
from rest_framework.serializers import ModelSerializer
from .models import Attempted, Score, StudentDetail
from educator.models import Story
from educator.serializers import EducatorDetailSerializer, QuestionSerializer

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

class AttemptSerializer(ModelSerializer):
    class Meta:
        model = Attempted
        fields = '__all__'

    def create(self, validated_data):
        question = Question.objects.get(id = validated_data.get('question').id)
        if question.answer == validated_data.get('answer'):
            validated_data['is_correct'] = True
        return Attempted.objects.create(**validated_data)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['attempted_answer'] = instance.answer
        response['correct_answer'] = instance.question.answer
        response.pop('answer')
        response['question'] = QuestionSerializer(instance.question).data
        response['question'].pop('id')
        response['question'].pop('quiz')
        response['question'].pop('answer')
        return response

class ScoreSerializer(ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['marks'] = instance.quiz.marks
        return response
