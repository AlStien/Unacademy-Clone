from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.EducatorCreateView.as_view()),
    path('series/', views.SeriesView.as_view()),
    # path('series/<int:pk>/', views.SeriesView.as_view()),
    path('series/lecture/', views.LectureView.as_view()),
    path('story/', views.StoryView.as_view())
]
