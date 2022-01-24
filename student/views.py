# ------ rest framework imports -------
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics 
from rest_framework import status
from django.shortcuts import get_object_or_404


from .serializers import AttemptSerializer, NotificationSerializer, StudentSerializer, StoryUserSerializer
from educator.serializers import SeriesSerializer, StorySerializer, EducatorDetailSerializer, QuizSerializer

from core.models import Notification
from .models import Attempted, StudentDetail
from educator.models import Series, Story, EducatorDetail, Quiz

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

# To view series list
class SeriesView(generics.ListAPIView):
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

# To view Educators List
class EducatorsView(generics.ListAPIView):
    serializer_class = EducatorDetailSerializer
    queryset = EducatorDetail.objects.all()

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
class NotificationView(generics.RetrieveDestroyAPIView):

    serializer_class = NotificationSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, receiver=self.request.user)
        return obj

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)

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

class QuizView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class AttemptView(generics.CreateAPIView):

    queryset = Attempted.objects.all()
    serializer_class = AttemptSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        data['student']=StudentDetail.objects.get(student=user).id
        _serializer = self.serializer_class(data=data)
        if _serializer.is_valid():
            _serializer.save()
            return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message':'User Already Exists or Required details not provided'}, status=status.HTTP_400_BAD_REQUEST) 

