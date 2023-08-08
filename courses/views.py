from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from courses.models import Lesson, Course, Payment
from courses.permissions import IsModerator
from courses.serializers import CourseSerializer, LessonSerializer, \
    PaymentSerializer


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
        self.permission_classes = [IsAuthenticated & ~IsModerator]
        return super().destroy(request, *args, **kwargs)


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Create DRF generic for :model:`courses.Lesson`
    """
    serializer_class = LessonSerializer
    # Define permissions
    permission_classes = [IsAuthenticated & ~IsModerator]


class LessonListAPIView(generics.ListAPIView):
    """
    List DRF generic for :model:`courses.Lesson`
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # Define permissions
    permission_classes = [IsAuthenticated | IsModerator]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Read DRF generic for :model:`courses.Lesson`
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    # Define permissions
    permission_classes = [IsAuthenticated | IsModerator]


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
    permission_classes = [IsAuthenticated & ~IsModerator]


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
