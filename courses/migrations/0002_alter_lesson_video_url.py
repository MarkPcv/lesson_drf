# Generated by Django 4.2.4 on 2023-08-05 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='video_url',
            field=models.URLField(verbose_name='video_url'),
        ),
    ]
