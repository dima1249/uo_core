from rest_framework import mixins, generics, permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, \
    CreateAPIView
from rest_framework.permissions import AllowAny
from django_filters import rest_framework as filters

from surgalt.filters import CourseFilter
from surgalt.models import CourseModel, TeacherModel
from surgalt.serializers import CourseSerializer, TeacherSerializer, RegisterCourseSerializer


class ListCreateCourseAPIView(ListCreateAPIView):
    serializer_class = CourseSerializer
    queryset = CourseModel.objects.all()
    permission_classes = [AllowAny]
    # pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CourseFilter

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class ListTeacherAPIView(ListAPIView):
    serializer_class = TeacherSerializer
    queryset = TeacherModel.objects.all()
    permission_classes = [AllowAny]
    # pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    # filterset_class = CourseFilter

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyCourseAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    queryset = CourseModel.objects.all()
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class RetrieveTeacherAPIView(RetrieveAPIView):
    serializer_class = TeacherSerializer
    queryset = TeacherModel.objects.all()
    permission_classes = [AllowAny]

class RegisterAPIView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegisterCourseSerializer
