import django_filters
from .models import Bookmark


class BookmarkFilter(django_filters.FilterSet):

    created_on = django_filters.DateFilter(field_name="created", lookup_expr="date")
    created = django_filters.DateFromToRangeFilter()

    expires_on = django_filters.DateFilter(field_name="expiry_date", lookup_expr="date")
    expires = django_filters.DateFromToRangeFilter(field_name="expiry_date")

    class Meta:
        model = Bookmark
        fields = ["created_on", "created", "expires_on", "expires"]
