from django_filters import rest_framework as filters
from rest_framework import serializers

from surgalt.models import CourseModel, TeacherModel, CourseRequestModel


class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.nick_name')
    type_name = serializers.ReadOnlyField(source='get_type_display')

    class Meta:
        model = CourseModel
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherModel
        fields = '__all__'


class RegisterCourseSerializer(serializers.ModelSerializer):
    created_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        print('RegisterCourseSerializer validate', data)
        # print('RegisterCourseSerializer role', data['student'].role)
        if data['created_user']:
            print(data['created_user'])
            raise serializers.ValidationError({"student": "user is not valid"})

        return data
        # if data['start_date'] > data['end_date']:
        #     raise serializers.ValidationError({"end_date": "finish must occur after start"})

    class Meta:
        model = CourseRequestModel
        fields = ['created_user',
                  'course',
                  'first_name',
                  'last_name',
                  'gender',
                  'birthday',
                  'start_date',
                  'end_date']

    # def save(self):
    #     user = CurrentUserDefault()
    #     title = self.validated_data['title']
    #     article = self.validated_data['article']

# class RegisterCourseSerializer(serializers.Serializer):
#     teacher = serializers.ReadOnlyField(source='teacher.nick_name')
