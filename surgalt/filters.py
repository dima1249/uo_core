from django_filters import rest_framework as filters

from surgalt.models import CourseModel


class CourseFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    type = filters.CharFilter(lookup_expr='icontains')
    # year = filters.NumberFilter()
    # year__gt = filters.NumberFilter(field_name='year', lookup_expr='gt')
    # year__lt = filters.NumberFilter(field_name='year', lookup_expr='lt')
    # creator__username = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CourseModel
        fields = ['teacher', 'type']