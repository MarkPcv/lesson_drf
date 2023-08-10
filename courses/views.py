from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from courses.models import Lesson, Course, Payment, Subscription
from courses.paginators import DefaultPaginator
from courses.permissions import IsModerator, IsOwner
from courses.serializers import CourseSerializer, LessonSerializer, \
    PaymentSerializer, SubscriptionSerializer, CourseSubSerializer
from users.models import UserRoles


class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD mechanism for :model:`courses.Course` using DRF
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    # Add pagination
    pagination_class = DefaultPaginator

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # Define permissions based on view action
        if self.action == 'retrieve':
            # Only Owner or Moderator can view this course
            permission_classes = [IsModerator | IsOwner]
        elif self.action == 'create':
            # All users (except moderators) can create lesson
            permission_classes = [~IsModerator]
        elif self.action == 'destroy':
            # Only Owner can delete this course
            permission_classes = [IsOwner]
        else:
            # All users (including moderators)
            permission_classes = []

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

    def retrieve(self, request, *args, **kwargs):
        """Override READ action"""

        # Check if user is NOT moderator
        if self.request.user.role != UserRoles.MODERATOR:
            serializer = CourseSubSerializer(self.get_object(), context={'request': request})
            return Response(serializer.data)
        return super().retrieve(request, *args, **kwargs)

    # def get_serializer_context(self):


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
    # Add pagination
    pagination_class = DefaultPaginator

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


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """
    Create DRF generic for :model:`courses.Subscription`
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    # All users (except moderators) can subscribe
    permission_classes = [~IsModerator]

    def perform_create(self, serializer):
        """Save user field during creation"""
        new_sub = serializer.save()
        new_sub.user = self.request.user
        new_sub.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """
    Delete DRF generic for :model:`courses.Subscription`
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    # All users (except moderators) can unsubscribe
    permission_classes = [~IsModerator]

    def destroy(self, request, *args, **kwargs):
        # Find course from DELETE request
        course = Course.objects.get(pk=self.kwargs.get('pk'))
        # Find instance of subscription for this course
        instance = Subscription.objects.get(user=request.user, course=course)
        # Delete instance from Database
        self.perform_destroy(instance)
        # Return HTTP response
        return Response(status=status.HTTP_204_NO_CONTENT)
