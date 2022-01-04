from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.EducatorCreateView.as_view()),
    path('series/', views.SeriesCreateView.as_view()),
]
