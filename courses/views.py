from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from courses.models import Lesson, Course, Payment
from courses.permissions import IsModerator, IsOwner
from courses.serializers import CourseSerializer, LessonSerializer, \
    PaymentSerializer
from users.models import UserRoles


class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD mechanism for :model:`courses.Course` using DRF
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    # Define permissions
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Override CREATE action"""
        # Define permissions
        self.permission_classes = [IsAuthenticated & ~IsModerator]
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Override DELETE action"""
        # Define permissions
        self.permission_classes = [IsAuthenticated & IsOwner]
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Save owner field during creation"""
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def list(self, request, *args, **kwargs):
        """Override LIST action"""
        # Check if user is NOT moderator
        if self.request.user.role != UserRoles.MODERATOR:
            self.queryset = Course.objects.filter(owner=self.request.user)
        else:
            self.queryset = Course.objects.all()
        return super().list(request, *args, **kwargs)


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Create DRF generic for :model:`courses.Lesson`
    """
    serializer_class = LessonSerializer
    # Define permissions
    permission_classes = [IsAuthenticated & ~IsModerator]

    def perform_create(self, serializer):
        """Save owner field during creation"""
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """
    List DRF generic for :model:`courses.Lesson`
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # Define permissions
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Method that return queryset for controller"""
        # Check if user is NOT moderator
        if self.request.user.role != UserRoles.MODERATOR:
            queryset = Lesson.objects.filter(owner=self.request.user)
        else:
            queryset = Lesson.objects.all()
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Read DRF generic for :model:`courses.Lesson`
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # Define permissions
    permission_classes = [IsAuthenticated | IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Update DRF generic for :model:`courses.Lesson`
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # Define permissions
    permission_classes = [IsAuthenticated | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Delete DRF generic for :model:`courses.Lesson`
    """
    queryset = Lesson.objects.all()
    # Define permissions
    permission_classes = [IsAuthenticated & IsOwner]


class PaymentListAPIView(generics.ListAPIView):
    """
    List DRF generic for :model:`courses.Payment`
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    # Adding filter modules
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Define ordering settings
    ordering_fields = ('date_paid',)
    # Define filtering settings
    filterset_fields = ('course', 'lesson', 'type',)
    # Define permissions
    permission_classes = [IsAuthenticated]
