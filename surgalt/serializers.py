from django_filters import rest_framework as filters
from rest_framework import serializers

from surgalt.models import CourseModel


class CourseSerializer(serializers.ModelSerializer):  # create class to serializer model
    teacher = serializers.ReadOnlyField(source='teacher.nick_name')
    type_name = serializers.ReadOnlyField(source='get_type_display')

    class Meta:
        model = CourseModel
        fields = '__all__'


