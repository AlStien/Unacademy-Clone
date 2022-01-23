from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.EducatorCreateView.as_view()),
    path('series/', views.SeriesView.as_view()),
    # path('series/<int:pk>/', views.SeriesView.as_view()),
    path('series/lecture/<int:pk>/', views.LectureView.as_view()),
    path('story/', views.StoryView.as_view()),
    path('quiz/', views.QuizView.as_view()),
    path('quiz/question/', views.QuestionCreateView.as_view()),
    path('quiz/<int:pk>/', views.QuestionListView.as_view())
]
