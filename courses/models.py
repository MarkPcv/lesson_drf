from django.db import models

from users.models import NULLABLE, User


class Course(models.Model):
    """
    Stores a single course entry.
    """
    name = models.CharField(max_length=100, verbose_name='name')
    preview = models.ImageField(**NULLABLE, verbose_name='image')
    description = models.TextField(verbose_name='description')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'course'
        verbose_name_plural = 'courses'
        ordering = ('name',)


class Lesson(models.Model):
    """
    Stores a single lesson entry, related to :model:`courses.Course`.
    """
    name = models.CharField(max_length=100, verbose_name='name')
    preview = models.ImageField(**NULLABLE, verbose_name='image')
    description = models.TextField(verbose_name='description')
    video_url = models.URLField(verbose_name='video_url', **NULLABLE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               verbose_name='course', related_name='lessons')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'
        ordering = ('name',)


class Payment(models.Model):
    """
    Stores a single payment entry, related to :model:`courses.Course`
    or to :model:`courses.Lesson`; and to :model:`users.User` .
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='user', related_name='payments')
    date_paid = models.DateTimeField(auto_now_add=True,
                                     verbose_name='date_paid')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE,
                               verbose_name='lesson')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE,
                               verbose_name='course')
    amount = models.PositiveIntegerField(verbose_name="amount")
    type = models.CharField(max_length=30, verbose_name="type")

    def __str__(self):
        if self.lesson:
            return f'{self.user.email} paid {self.amount} for Lesson "{self.lesson.name}" via {self.type}'
        return f'{self.user.email} paid {self.amount} for Course "{self.course.name}" via {self.type}'

    class Meta:
        verbose_name = 'payment'
        verbose_name_plural = 'payments'
        ordering = ('-date_paid',)
