# ------ rest framework imports -------
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import EducatorDetailSerializer, LectureSerializer, QuestionSerializer, QuizSerializer, SeriesSerializer, StorySerializer

from .models import EducatorDetail, Lecture, Question, Quiz, Series, Story

from django.utils import timezone

# to create and educator by providing the details
class EducatorCreateView(APIView):

    def get(self, request):
        serializer = EducatorDetailSerializer(instance = EducatorDetail.objects.get(educator = request.user))
        return Response(serializer.data)

    def post(self, request, format=None):
        data = (request.data).copy()
        user = request.user
        if data.get('name') is None:
            data['name'] = user.name
        data["educator"] = user.id
        serializer = EducatorDetailSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user.is_educator = True
            user.name = data.get('name')
            user.save()
        # re defining to get the updated values of user model with educator details
        serializer = EducatorDetailSerializer(instance = EducatorDetail.objects.get(educator = request.user))
        return Response(serializer.data)
    
    def put(self, request):
        data = (request.data).copy()
        data['educator'] = request.user.id
        serializer = EducatorDetailSerializer(instance = EducatorDetail.objects.get(educator = request.user), data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

# to upload a series and get the list of all series belong to the user
class SeriesView(APIView):
    
    def get(self, request):
        user = request.user
        if user.is_educator :
            try:
                data = Series.objects.filter(educator = user)
                serializer = SeriesSerializer(data, many=True)
                return Response(serializer.data)
            except:
                return Response({'message':'No courses found'}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({'message':'User not a educator'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        user = request.user
        if user.is_educator :
            data = (request.data).copy()
            data['educator'] = user.id
            data['name'] = data.get('name')+ ' by ' + user.name
            serializer = SeriesSerializer(data = data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            response = serializer.data
            return Response(response)

        else:
            return Response({'message':'User not a educator'}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        user = request.user
        if user.is_educator:
            data = (request.data).copy()
            data['educator'] = user
            print(user)
            print(data)
            serializer = SeriesSerializer(instance=Series.objects.get(id = request.data.get('id',)), data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data)
        else:
            return Response({'message':'User not a educator'}, status=status.HTTP_401_UNAUTHORIZED)

#to upload lectures to a series and get their list
class LectureView(generics.ListCreateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer

    def get(self, request, pk):
        qs = Lecture.objects.filter(series=pk)
        print(qs)
        serializer = LectureSerializer(instance=qs, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        user = request.user
        if user.is_educator:
            data = (request.data).copy()
            data['series'] = pk
            series = Series.objects.get(id = pk)
            serializer = LectureSerializer(data = data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                series.lectures = series.lectures + 1
                series.save()
            return Response(serializer.data)
        else:
            return Response({'message':'User not a educator'}, status=status.HTTP_401_UNAUTHORIZED)

# to upload and view stories
class StoryView(APIView):
    
    def get(sel, request):
        user = request.user
        if user.is_educator:
            data = Story.objects.filter(educator = user.id, time_created__gte = timezone.now() - timezone.timedelta(days=1))
            if not data:
                return Response({'message':'No Stories available'}, status=status.HTTP_204_NO_CONTENT)
            serializer = StorySerializer(instance=data, many=True)
            return Response(serializer.data)
        else:
            return Response({'message':'User not a educator'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        user = request.user
        if user.is_educator:
            data = request.data.copy()
            data['educator'] = user.id
            serializer = StorySerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data)
        else:
            return Response({'message':'User not a educator'}, status=status.HTTP_401_UNAUTHORIZED)

# to create a quiz
class QuizView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(educator = self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_educator:
            data = request.data.copy()
            data['educator']=user.id
            _serializer = self.serializer_class(data=data)
            if _serializer.is_valid():
                _serializer.save()
                return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message':'Title not Unique or Required details not provided'}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({'message':'User not an educator'}, status=status.HTTP_401_UNAUTHORIZED) 
        
# to create questions for a quiz
class QuestionCreateView(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data.copy()
        quiz = Quiz.objects.get(id = data.get('quiz'))
        if quiz.educator == user:
            _serializer = self.serializer_class(data=data)
            if _serializer.is_valid():
                _serializer.save()
                quiz.questions += 1
                quiz.save()
                return Response(data=_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'message':'Required details not provided'}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({'message':'User Not an educator or did not create the quiz'}, status=status.HTTP_400_BAD_REQUEST) 

# to view questions of a quiz
class QuestionListView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(quiz=self.kwargs['pk'])

