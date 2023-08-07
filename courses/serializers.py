from rest_framework import serializers
from rest_framework.fields import IntegerField

from courses.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = IntegerField(source='lesson_set.count', required=False)
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = '__all__'
