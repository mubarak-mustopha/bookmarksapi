from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from .filters import BookmarkFilter
from .models import Bookmark, Collection
from .permissions import IsOwner
from .serializers import (
    BookmarkSerializer,
    ReadOnlyBookmarkSeriaizer,
    CollectionSerializer,
    ReadOnlyCollectionSerializer,
)


# Create your views here.
class CollectionModelViewSet(ModelViewSet):
    serializer_class = CollectionSerializer
    queryset = Collection.objects.prefetch_related("children", "bookmark_set")

    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadOnlyCollectionSerializer
        return self.serializer_class

    def get_queryset(self):
        base_queryset = self.queryset
        return base_queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    @action(detail=True, methods=["GET"])
    def children(self, request, pk):
        base_collection = self.get_object()
        children = base_collection.children.all()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(children, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET"])
    def bookmarks(self, request, pk):
        base_collection = self.get_object()
        bookmarks = base_collection.bookmark_set.all()

        serializer = ReadOnlyBookmarkSeriaizer(instance=bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookmarkViewSet(ModelViewSet):
    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.prefetch_related("collection", "tags")

    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = BookmarkFilter
    search_fields = ["title", "tags__name"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadOnlyBookmarkSeriaizer
        return BookmarkSerializer

    def get_queryset(self):
        base_queryset = self.queryset
        return base_queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
