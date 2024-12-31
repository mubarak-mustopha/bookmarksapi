from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


from .models import Tag


class BaseTagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "owner",
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Tag.objects.all(),
                fields=("name", "owner"),
            )
        ]

    def validate_name(self, value):
        return slugify(value)


class TagSerializer(BaseTagSerializer):
    bookmarks_count = serializers.SerializerMethodField()

    class Meta(BaseTagSerializer.Meta):
        fields = ["id", "name", "owner", "bookmarks_count"]

    def get_bookmarks_count(self, obj) -> int:
        return obj.bookmarks.count()
