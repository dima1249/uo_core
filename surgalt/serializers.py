from datetime import timedelta

from django_filters import rest_framework as filters
from rest_framework import serializers

from account.models import GENDER
from surgalt.models import CourseModel, TeacherModel, CourseRequestModel, CourseStudentModel, StudentVideoModel


class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.nick_name')
    type_name = serializers.ReadOnlyField(source='get_type_display')

    class Meta:
        model = CourseModel
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    level_name = serializers.ReadOnlyField(source='get_level_display')

    class Meta:
        model = TeacherModel
        fields = '__all__'


class StudentVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentVideoModel
        fields = '__all__'


class CourseStudentSerializer(serializers.ModelSerializer):
    # level_name = serializers.ReadOnlyField(source='get_level_display')
    course = CourseSerializer()
    videos = StudentVideoSerializer(many=True)

    class Meta:
        model = CourseStudentModel
        fields = [
            "id",
            "active",
            "start_date",
            "end_date",
            "first_name",
            "last_name",
            "gender",
            "birthday",
            "payment_date",
            "desc",
            "course",
            "videos",
        ]


class RegisterCourseSerializer(serializers.ModelSerializer):
    created_user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    first_name = serializers.CharField(required=True, max_length=100)
    last_name = serializers.CharField(required=True, max_length=100)
    gender = serializers.ChoiceField(required=True, choices=GENDER)
    birthday = serializers.DateField(required=True)
    start_date = serializers.DateField(required=True)

    def validate(self, data):
        print('RegisterCourseSerializer validate', data)
        # print('RegisterCourseSerializer role', data['student'].role)
        if not data['created_user']:
            raise serializers.ValidationError({"student": "user is not valid"})

        if not "end_date" in data:
            data['end_date'] = data['start_date'] + timedelta(days=30)

        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError({"end_date": "Эхлэх өдрөөс хойш байх естой"})
        # 'course', 'first_name', 'last_name', 'gender', 'birthday', 'start_date'
        if CourseRequestModel.objects.filter(course=data['course'], first_name=data['first_name'],
                                             last_name=data['last_name'], gender=data['gender'],
                                             birthday=data['birthday'], start_date=data['start_date'],
                                             status=1).count():
            raise serializers.ValidationError({"model": "Ижил хүсэлт хүлээгдэж байна."})
        return data

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
