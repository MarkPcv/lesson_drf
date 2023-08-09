from rest_framework import serializers
from rest_framework.fields import IntegerField

from courses.models import Lesson, Course, Payment, Subscription
from courses.validators import validate_url


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for :model:`courses.Lesson`
    """
    # Add validator to lesson field
    video_url = serializers.URLField(validators=[validate_url])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for :model:`courses.Course`
    """
    # Number of lessons in the course
    lesson_count = IntegerField(source='lesson_set.count', required=False)
    # List of lessons in the course
    lessons = LessonSerializer(many=True, required=False)

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for :model:`courses.Payment`
    """
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for :model:`courses.Subscription`
    """
    class Meta:
        model = Subscription
        fields = '__all__'


class CourseSubSerializer(serializers.ModelSerializer):
    """
    Serializer for course :model:`courses.Course`
    That includes subscription field for user
    """
    # Number of lessons in the course
    lesson_count = IntegerField(source='lesson_set.count', required=False)
    # List of lessons in the course
    lessons = LessonSerializer(many=True, required=False)
    # Subscription status
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_is_subscribed(self, instance):
        request = self.context['request']
        subscription = Subscription.objects.filter(user=request.user,
                                                   course=instance)
        if subscription:
            return True
        return False