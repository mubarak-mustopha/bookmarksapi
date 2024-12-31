from django.urls import path
from rest_framework import routers

from .views import (
    BookmarkViewSet,
    CollectionModelViewSet,
)


router = routers.SimpleRouter()
router.register(r"bookmarks", BookmarkViewSet)
router.register(r"collections", CollectionModelViewSet)

urlpatterns = router.urls
