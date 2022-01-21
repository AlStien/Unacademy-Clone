from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.StudentCreateView.as_view()),
    path('profile/', views.StudentDetailView.as_view()),
    path('series/', views.SeriesView.as_view()),
    path('series/lecture/', views.LectureView.as_view()),
    path('educator-list/', views.EducatorsView.as_view()),
    path('educator-profile/<int:pk>/', views.EducatorDetailsView.as_view()),
    path('wishlist/', views.WishlistView.as_view()),
    path('notification/', views.NotificationView.as_view())
]
