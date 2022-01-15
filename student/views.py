# ------ rest framework imports -------
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics 
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import StudentSerializer

from .models import StudentDetail

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

class StudentDetailView(generics.RetrieveUpdateAPIView):
    queryset = StudentDetail.objects.all()
    serializer_class = StudentSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, student=self.request.user)
        return obj

        