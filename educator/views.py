# ------ rest framework imports -------
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import EducatorDetailSerializer

class EducatorCreateView(APIView):

    def post(self, request):
        data = request.data
        data['educator'] = request.user
        serializer = EducatorDetailSerializer(data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return serializer.data