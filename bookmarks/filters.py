import django_filters
from .models import Bookmark


class BookmarkFilter(django_filters.FilterSet):

    date_created = django_filters.DateFilter(field_name="created", lookup_expr="date")
    date_created__lt = django_filters.DateFilter(
        field_name="created", lookup_expr="date__lt"
    )
    date_created__gt = django_filters.DateFilter(
        field_name="created", lookup_expr="date__gt"
    )

    class Meta:
        model = Bookmark
        fields = {
            "expiry_date": [
                "date",
                "date__gt",
                "date__lt",
            ],
        }
