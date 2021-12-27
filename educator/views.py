# ------ rest framework imports -------
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import EducatorDetailSerializer

from core.models import User
from .models import EducatorDetail

class EducatorCreateView(APIView):

    def get(self, request):
        user = request.user
        serializer = EducatorDetailSerializer(instance = EducatorDetail.objects.get(educator = request.user))
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user
        data['educator'] = user.id
        serializer = EducatorDetailSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user.is_educator = True
            user.save()
        return Response(serializer.data)
    
    def put(self, request):
        data = request.data
        data['educator'] = request.user.id
        serializer = EducatorDetailSerializer(instance = EducatorDetail.objects.get(educator = request.user), data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
