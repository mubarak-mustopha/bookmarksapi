from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Tag
from .serializers import BaseTagSerializer, TagSerializer


# Create your views here.
class TagModelViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TagSerializer
        return BaseTagSerializer

    def get_queryset(self):
        base_queryset = self.queryset

        return base_queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action == "detail":
            return permissions + [IsOwner()]

        return permissions

    @action(methods=["GET"], detail=True)
    def bookmarks(self, request, pk):
        tag_obj = self.get_object()
        tag_bookmarks = tag_obj.bookmarks.all()

        serializer = ReadOnlyBookmarkSeriaizer(tag_bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.settings import api_settings
