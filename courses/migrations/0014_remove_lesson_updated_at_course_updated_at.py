# Generated by Django 4.2.4 on 2023-08-19 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_lesson_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='course',
            name='updated_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='updated_time'),
        ),
    ]
