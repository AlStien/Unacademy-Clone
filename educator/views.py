# ------ rest framework imports -------
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import EducatorDetailSerializer, SeriesSerializer

from .models import EducatorDetail, Series

class EducatorCreateView(APIView):

    def get(self, request):
        serializer = EducatorDetailSerializer(instance = EducatorDetail.objects.get(educator = request.user))
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        user = request.user
    # mutable data for when data is being passed as form-data
        # _mutable = data._mutable
        # # set to mutable
        # data._mutable = True
        # # сhange the values
        if data.get('name') is None:
            data['name'] = user.name
        data["educator"] = user.id
        # # set mutable flag back
        # data._mutable = _mutable

        serializer = EducatorDetailSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user.is_educator = True
            user.name = data.get('name')
            user.save()
        serializer = EducatorDetailSerializer(instance = EducatorDetail.objects.get(educator = request.user))
        return Response(serializer.data)
    
    def put(self, request):
        data = request.data
        data['educator'] = request.user.id
        serializer = EducatorDetailSerializer(instance = EducatorDetail.objects.get(educator = request.user), data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

class SeriesCreateView(APIView):
    
    def get(self, request):
        user = request.user
        if user.is_educator :
            try:
                id = request.data.get('id',)
                serializer = SeriesSerializer(instance=Series.objects.get(id = id))
                return Response(serializer.data)
            except:
                return Response({'message':'No such course exists'}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({'message':'User not a educator'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        user = request.user
        if user.is_educator :
            data = request.data
            data['educator'] = user.id
            serializer = SeriesSerializer(data = data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data)

        else:
            return Response({'message':'User not a educator'}, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        user = request.user
        if user.is_educator:
            print("gg")
            data = request.data
            data['educator'] = user
            print(user)
            print(data)
            serializer = SeriesSerializer(instance=Series.objects.get(id = request.data.get('id',)), data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data)
        else:
            return Response({'message':'User not a educator'}, status=status.HTTP_401_UNAUTHORIZED)
