from django.contrib import admin
from django.urls import path, include
from core.views import getRoutes
# For JWT Tokens
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', getRoutes, name='Get Routes'),
    path('admin/', admin.site.urls),
    # Token APIs
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    # Educator App APIs
    path('educator/', include('educator.urls')),

    # oauth
    # path('auth/', include('drf_social_oauth2.urls', namespace='drf'))
]
