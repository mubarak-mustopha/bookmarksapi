from django.urls import path
from rest_framework import routers

from .views import TagModelViewSet

router = routers.SimpleRouter()
router.register(r"", TagModelViewSet)

urlpatterns = router.urls
