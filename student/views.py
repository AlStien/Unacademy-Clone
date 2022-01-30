# ------ rest framework imports -------
from ast import Delete
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, mixins 
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from .serializers import AttemptSerializer, NotificationSerializer, ScoreSerializer, StudentSerializer, StoryUserSerializer
from educator.serializers import SeriesSerializer, StorySerializer, EducatorDetailSerializer, QuizSerializer

from core.models import Notification
from .models import Attempted, StudentDetail, Score
from educator.models import Series, Story, EducatorDetail, Quiz, Question

# To create Student Profile
class StudentCreateView(generics.CreateAPIView):
    queryset = StudentDetail.objects.all()
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        data['student']=user.id
        _serializer = self.serializer_class(data=data)
        if _serializer.is_valid():
            _serializer.save()
            user.is_student = True
            user.name = data.get('name')
            user.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message':'User Already Exists or Required details not provided'}, status=status.HTTP_400_BAD_REQUEST) 

# To view and edit student profilea
class StudentDetailView(generics.RetrieveUpdateAPIView):
    queryset = StudentDetail.objects.all()
    serializer_class = StudentSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, student=self.request.user)
        return obj

    def put(self, request, *args, **kwargs):
        student = StudentDetail.objects.get(student = request.user)
        remove = request.data.get('remove')
        if remove is not None:
            student.following.remove(remove)
            student.save()
        following = request.data.get('following')
        if following is not None:
            student.following.add(following)
            student.save()
        serializer = StudentSerializer(instance=student)
        return Response(serializer.data)

# To view series list
class SeriesView(generics.ListAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs).data.copy()
        for d in response:
            d['is_wishlisted'] = False
            series = Series.objects.get(id = d['id'])
            d['is_wishlisted'] = False
            if StudentDetail.objects.filter(student = request.user, wishlist = series).exists():
                d['is_wishlisted'] = True
            print(response)
        return Response(response)

# To view Educators List
class EducatorsView(generics.ListAPIView):
    serializer_class = EducatorDetailSerializer
    queryset = EducatorDetail.objects.all()

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs).data
        for d in response:
            d['is_followed'] = False
            educator = EducatorDetail.objects.get(id = d['id'])
            d['is_followed'] = False
            if StudentDetail.objects.filter(student = request.user, following = educator).exists():
                d['is_followed'] = True
            print(response)
        return Response(response)

# To view Educator's Profile
class EducatorDetailsView(generics.RetrieveAPIView):
    queryset = EducatorDetail.objects.all()
    serializer_class = EducatorDetailSerializer

# Wishlist of a student
class WishlistView(APIView):

    def get(self, request, format=None):
        student = StudentDetail.objects.get(student=request.user.id)
        series = Series.objects.filter(wishlist = student)
        serializer = SeriesSerializer(series, many = True)
        response = serializer.data
        
        for d in response:
            d['is_wishlisted'] = False
            series = Series.objects.get(id = d['id'])
            d['is_wishlisted'] = False
            if StudentDetail.objects.filter(student = request.user, wishlist = series).exists():
                d['is_wishlisted'] = True

        return Response(serializer.data)
    
    def put(self, request, format=None):
        student = StudentDetail.objects.get(student = request.user)
        series = Series.objects.get(id = request.data.get('series'))
        if StudentDetail.objects.filter(wishlist = series, student=request.user).exists():
            return Response({'message': 'Series Already in Wishlist'}, status=status.HTTP_208_ALREADY_REPORTED)
        student.wishlist.add(series)
        return Response(data = {'message': 'Series added to wishlist'}, status=status.HTTP_201_CREATED)

    def delete(self, request, format = None):
        student = StudentDetail.objects.get(student = request.user)
        series = Series.objects.get(id = request.data.get('series'))
        if StudentDetail.objects.filter(wishlist = series, student=request.user).exists():
            student.wishlist.remove(series)
            return Response({'message': 'Series Removed from Wishlist'}, status=status.HTTP_208_ALREADY_REPORTED)
        else:
            return Response({'message': 'Series Not in Wishlist'}, status = status.HTTP_404_NOT_FOUND)

# To view Notifications
class NotificationView(generics.GenericAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin):

    serializer_class = NotificationSerializer
    # pagination_class = PageNumberPagination

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, receiver=self.request.user)
        print(obj)
        return obj

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# To view Stories of educators
class StoryUserView(generics.ListAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryUserSerializer

# To view Stories of educators
class StoryView(generics.ListAPIView):
    serializer_class = StorySerializer

    def get_queryset(self):
        qs = Story.objects.filter(educator = self.kwargs['pk'])
        return qs

# To view all quizes
class QuizView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get(self, request, *args, **kwargs):
        qs = super().get(request, *args, **kwargs)
        for q in qs.data:
            q['is_attempted'] = False
            if Score.objects.filter(student = StudentDetail.objects.get(student = request.user), quiz = Quiz.objects.get(id = q['id'])).exists():
                q['is_attempted'] = True
        return qs

# To answer a question in a quiz
class AttemptView(generics.CreateAPIView):

    queryset = Attempted.objects.all()
    serializer_class = AttemptSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        student = StudentDetail.objects.get(student=user)
        data['student']=student.id
    
        # to increase the score, getting the score object
        question = Question.objects.get(id = data.get('question'))
        quiz = Quiz.objects.get(id = question.quiz.id)
        if Score.objects.filter(student = student.id, quiz = quiz).exists():
            score = Score.objects.get(student = student.id, quiz = quiz)
        else:
            score = Score.objects.create(student = student, quiz = quiz, score = 0)

        _serializer = self.serializer_class(data=data)
        if _serializer.is_valid():
            _serializer.save()
            if _serializer.data.get('is_correct'):
                score.score += question.marks   # adding the score for the quiz
                score.save()
            print(_serializer.data)
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message':'Required details not provided'}, status=status.HTTP_400_BAD_REQUEST) 

# Quiz's Questions analysis
class AttemptedQuestionsView(generics.ListAPIView):
    serializer_class = AttemptSerializer

    def get_queryset(self):
        return Attempted.objects.filter(student = StudentDetail.objects.get(student = self.request.user), 
                        question__in = Question.objects.filter(quiz = Quiz.objects.get(id = self.kwargs['pk'])))

# Final Score of a student in a quiz
class ScoreView(generics.ListAPIView):

    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def get_queryset(self):
        return Score.objects.filter(student = StudentDetail.objects.get(student = self.request.user).id, quiz = Quiz.objects.get(id = self.kwargs['pk']).id)
