import datetime

from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from config.tasks import send_notification
from courses.models import Lesson, Course, Payment, Subscription
from courses.paginators import DefaultPaginator
from courses.permissions import IsModerator, IsOwner
from courses.serializers import CourseSerializer, LessonSerializer, \
    PaymentSerializer, SubscriptionSerializer, CourseSubSerializer, \
    PaymentRetrieveSerializer
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

    def update(self, request, *args, **kwargs):
        """Override UPDATE action to notify subscribers of course"""

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # Get list of all subscribers
        subscription_list = Subscription.objects.filter(course=instance)
        # Check if at least one subscriber exists
        if subscription_list:
            for subscription in subscription_list:
                # Send mail to each subscriber
                send_notification.delay(
                    subscription.course.name,
                    subscription.user.email
                )

        return Response(serializer.data)


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

    def perform_update(self, serializer):
        updated_lesson = serializer.save()
        updated_lesson.save()
        # Get course
        course = Course.objects.get(pk=updated_lesson.course_id)
        # Record previous update time
        prev_update_time = course.updated_at if course.updated_at else 0
        # Add new update time (UTC)
        course.updated_at = datetime.datetime.now()
        course.save()
        # Send notification if last update was more than 4 hours ago
        # Moscow - UTC time
        if course.updated_at - prev_update_time.replace(tzinfo=None) > datetime.timedelta(hours=7):
            # Get list of all subscribers
            subscription_list = Subscription.objects.filter(course=course)
            # Check if at least one subscriber exists
            if subscription_list:
                for subscription in subscription_list:
                    # Send mail to each subscriber
                    send_notification.delay(
                        subscription.course.name,
                        subscription.user.email
                    )


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


class PaymentCreateAPIView(generics.CreateAPIView):
    """
    Create DRF generic for :model:`courses.Payment`
    """
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """Save user and course field during creation"""
        new_payment = serializer.save()
        new_payment.user = self.request.user
        new_payment.course = Course.objects.get(pk=self.kwargs.get('pk'))
        new_payment.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """
    Retrieve DRF generic for :model:`courses.Payment`
    """
    serializer_class = PaymentSerializer

    def get_object(self):
        obj = Payment.objects.get(
            user=self.request.user,
            course=Course.objects.get(pk=self.kwargs.get('pk'))
        )
        return obj


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
