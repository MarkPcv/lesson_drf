import datetime

from celery import shared_task
from celery.app import task
from django.conf import settings
from django.core.mail import send_mail

from courses.services import log_trial
from users.models import User


@shared_task
def send_notification(course_title: str, email: str) -> None:
    """
    Sends notification to the subscriber of the course
    """
    send_mail(
        subject='Course Updated',
        message=f'Hi!\n\nCourse {course_title} has been updated.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )


@shared_task
def check_login():
    """
    Checks when user was logged last time
    Makes inactive if necessary
    """
    # Get list of users
    users = User.objects.all()
    # Check last login datetime for each user
    for user in users:
        # log_trial(user)
        if user.last_login:
            # Get current time
            now = datetime.datetime.now()
            # Get user last login time
            last_login = user.last_login
            # Get difference between current and last login times
            diff = now - last_login.replace(tzinfo=None) + datetime.timedelta(hours=3)
            # Check if user has logged for more than 1 month
            if diff > datetime.timedelta(days=30):
                user.is_active = False
                user.save()

