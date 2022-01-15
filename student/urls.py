from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.StudentCreateView.as_view()),
]
