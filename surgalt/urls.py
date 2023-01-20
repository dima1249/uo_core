from django.urls import path
from .views import *

urlpatterns = [
    path('teacher/', ListTeacherAPIView.as_view(), name='get_teachers'),
    path('teacher/<int:pk>/', RetrieveTeacherAPIView.as_view(), name='get_teacher'),
    path('course/', ListCreateCourseAPIView.as_view(), name='get_post_course'),
    path('course/register', RegisterAPIView.as_view(), name='register_course'),
    path('course/<int:pk>/', RetrieveUpdateDestroyCourseAPIView.as_view(), name='get_delete_update_course'),

    path('student/', ListStudentAPIView.as_view(), name='get_course_student_list'),
    path('student/<int:pk>/', GetStudentAPIView.as_view(), name='get_course_student'),
    # path('students/<int:pk>/', RetrieveUpdateDestroyCourseAPIView.as_view(), name='get_update_course'),

]