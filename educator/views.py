# ------ rest framework imports -------
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status

from .serializers import EducatorDetailSerializer, LectureSerializer, SeriesSerializer

from .models import EducatorDetail, Lecture, Series

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

# to get the details of a series
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

class LectureView(APIView):

    def get(self, request):
        user = request.user
        data = (request.data).copy()
        lectures = Lecture.objects.filter(series = data.get('series'))
        serializer = LectureSerializer(instance = lectures, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        if user.is_educator:
            data = (request.data).copy()
            serializer = LectureSerializer(data = data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data)
        else:
            return Response({'message':'User not a educator'}, status=status.HTTP_401_UNAUTHORIZED)