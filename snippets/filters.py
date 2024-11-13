from django_filters import rest_framework as filters
from .models import Snippet

class SnippetFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    created = filters.DateFromToRangeFilter()

    class Meta:
        model = Snippet
        fields = ['title', 'created']