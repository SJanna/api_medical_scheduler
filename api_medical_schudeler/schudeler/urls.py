from django.urls import include, path
from rest_framework import routers
from .views import PersonaViewSet, CitasViewSet

router = routers.DefaultRouter()
router.register(r'personas', PersonaViewSet)
router.register(r'citas', CitasViewSet)

urlpatterns = [
    path('', include(router.urls)),
]