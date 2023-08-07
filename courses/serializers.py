from rest_framework import serializers
from rest_framework.fields import IntegerField

from courses.models import Lesson, Course, Payment


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for :model:`courses.Lesson`
    """
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
    lessons = LessonSerializer(many=True)

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
