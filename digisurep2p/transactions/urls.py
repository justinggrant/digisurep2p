from django.urls import include, path
from rest_framework import routers

from .api.views import TransactionViewSet

app_name = "transactions"

router = routers.DefaultRouter()
router.register("", TransactionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
