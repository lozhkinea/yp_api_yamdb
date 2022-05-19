import django_filters
from reviews.models import Title

class TitleFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter(name="genre", lookup_type="slug")

    class Meta:
        model = Title
        fields = ['genre']
        # fields = {
        #     'category__slug': ['exact'],
        #     'genre__slug': ['exact'],
        #     'name': ['exact'],
        #     'year': ['exact'],
        # }