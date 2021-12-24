from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view
# For JWT Tokens
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# to show all the available routes
@api_view(['GET'])
def getRoutes(request):
    routes = [
        'admin/',
        'educator/'
    ]

    return Response(routes)

# urls
urlpatterns = [
    path('', getRoutes, name='Get Routes'),
    path('admin/', admin.site.urls),
    # Token APIs
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    # Educator App APIs
    path('educator/', include('core.urls')),
    path('educator/', include('educator.urls')),

    # oauth
    # path('auth/', include('drf_social_oauth2.urls', namespace='drf'))
]
