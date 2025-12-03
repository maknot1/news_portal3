import django_filters
from .models import News

class NewsFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Название содержит')
    author = django_filters.CharFilter(field_name='author__username', lookup_expr='icontains', label='Автор')
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='После даты')

    class Meta:
        model = News
        fields = ['title', 'author', 'created_at']
