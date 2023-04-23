from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.forms.models import model_to_dict

from surgalt.models import CourseStudentModel, CourseRequestModel
from surgalt.serializers import SaveCourseStudentSerializer


@receiver(pre_save, sender=CourseRequestModel)
def update_course_student(sender, instance, *args, **kwargs):
    if instance.id:
        previous = CourseRequestModel.objects.get(id=instance.id)
        if instance.status == 4 and previous.status != instance.status:
            print('status update', instance.status)
            students = CourseStudentModel.objects.filter(
                first_name=instance.first_name,
                last_name=instance.last_name,
                gender=instance.gender,
                birthday=instance.birthday,
                course=instance.course,
            )
            if len(students) > 0:
                print('students exist ')
                student = students[0]
                student.start_date = instance.start_date
                student.end_date = instance.end_date
                student.payment_date = instance.payment_date
                student.save()
            else:
                _data = model_to_dict(instance, fields=['first_name',
                                                        'last_name',
                                                        'gender',
                                                        'birthday',
                                                        'start_date',
                                                        'end_date',
                                                        'payment_date',
                                                        'desc',
                                                        ])
                _data['created_user'] = instance.created_user.id
                _data['course'] = instance.course.id

                print('_data ', _data)
                course_student_serializer = SaveCourseStudentSerializer(data=_data)
                if course_student_serializer.is_valid():
                    course_student_serializer.save()
                else:
                    print('courseStudentSerializer Error: ', course_student_serializer.errors)
        else:
            print('status update', instance.status)
