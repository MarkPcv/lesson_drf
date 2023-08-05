from django.db import models

from users.models import NULLABLE


class Course(models.Model):
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
    name = models.CharField(max_length=100, verbose_name='name')
    preview = models.ImageField(**NULLABLE, verbose_name='image')
    description = models.TextField(verbose_name='description')
    video_url = models.URLField(verbose_name='video_url')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'
        ordering = ('name',)
