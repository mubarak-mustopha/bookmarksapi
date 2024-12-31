from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


from tag.serializers import BaseTagSerializer
from .models import Bookmark, Collection


class MiniCollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ("id", "name")
        read_only_fields = ("id", "name")


class CollectionSerializer(serializers.ModelSerializer):

    collections_count = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Collection
        fields = (
            "id",
            "name",
            "owner",
            "description",
            "parent",
            "collections_count",
            "bookmarks_count",
            "created",
            "updated",
        )
        read_only_fields = ("created", "updated")
        validators = [
            UniqueTogetherValidator(
                queryset=Collection.objects.all(),
                fields=("name", "owner"),
            )
        ]

    def get_collections_count(self, obj) -> int:
        return obj.children.count()

    def get_bookmarks_count(self, obj) -> int:
        return obj.bookmark_set.count()


class ReadOnlyCollectionSerializer(CollectionSerializer):
    parent = MiniCollectionSerializer()


class BookmarkSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Bookmark
        fields = "__all__"
        read_only_fields = (
            "created",
            "updated",
        )

        extra_kwargs = {
            "tags": {"required": False},
        }

        validators = [
            UniqueTogetherValidator(
                queryset=Bookmark.objects.all(),
                fields=("title", "owner"),
            )
        ]


class ReadOnlyBookmarkSeriaizer(BookmarkSerializer):
    tags = BaseTagSerializer(many=True, read_only=True)
    collection = MiniCollectionSerializer()
