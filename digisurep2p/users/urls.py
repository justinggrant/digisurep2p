from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api.views import UserViewSet

app_name = "users"
router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
