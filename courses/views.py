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

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # Define permissions based on view action
        if self.action == 'list':
            # List is shown to any authorized personnel
            permission_classes = [IsAuthenticated]
        elif self.action == 'retrieve':
            # Only Owner or Moderator can view this course
            permission_classes = [IsModerator | IsOwner]
        elif self.action == 'create':
            # All users (except moderators) can create lesson
            permission_classes = [~IsModerator]
        elif self.action == 'destroy':
            # Only Owner can delete this course
            permission_classes = [IsOwner]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Save owner field during creation"""
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def list(self, request, *args, **kwargs):
        """Override LIST action"""
        # Check if user is NOT moderator
        if self.request.user.role != UserRoles.MODERATOR:
            # Return the list of user's courses
            self.queryset = Course.objects.filter(owner=self.request.user)
        else:
            # Return all courses
            self.queryset = Course.objects.all()
        return super().list(request, *args, **kwargs)


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Create DRF generic for :model:`courses.Lesson`
    """
    serializer_class = LessonSerializer
    # Define permissions
    # All users (except moderators) can create lesson
    permission_classes = [~IsModerator]

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

    def get_queryset(self):
        """Method that return queryset for controller"""
        # Check if user is NOT moderator
        if self.request.user.role != UserRoles.MODERATOR:
            # Return the list of user's lessons
            queryset = Lesson.objects.filter(owner=self.request.user)
        else:
            # Return all lessons
            queryset = Lesson.objects.all()
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Read DRF generic for :model:`courses.Lesson`
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # Define permissions:
    # Only Owner or Moderator can view this lesson
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Update DRF generic for :model:`courses.Lesson`
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # Define permissions
    # Only Owner or Moderator can edit this lesson
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Delete DRF generic for :model:`courses.Lesson`
    """
    queryset = Lesson.objects.all()
    # Define permissions
    # Only Owner can delete this lesson
    permission_classes = [IsOwner]


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
