from django.contrib import admin
from django.urls import path, include
# For JWT Tokens
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Token APIs
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    # Educator App APIs
    path('educator/', include('educator.urls')),
]
